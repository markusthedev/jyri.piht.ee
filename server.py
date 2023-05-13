import os
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import datetime
import logging
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') 
socketio = SocketIO(app)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[logging.FileHandler('server_logs.txt', 'a'), logging.StreamHandler()]
)

def log_request(request):
    client_ip = request.remote_addr

    request_method = request.method
    request_path = request.path
    request_data = request.get_data().decode('utf-8')

    logging.info(f"IP: {client_ip} | Method: {request_method} | Path: {request_path} | Data: {request_data}")


def save_message_to_file(message, chatroom):
    filename = 'piht.txt' if chatroom == 'piht' else 'chat_history.txt'
    with open(filename, 'a') as f:
        f.write(f"{message}\n")

def load_chat_history_from_file(chatroom):
    filename = 'piht.txt' if chatroom == 'piht' else 'chat_history.txt'
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            messages = []
            for line in f.readlines():
                username, content = line.strip().split(": ", 1)
                messages.append({"username": username, "content": content, "chatroom": chatroom})
            return messages
    return []

def save_log(log_entry, log_type='access'):
    client_ip = request.remote_addr
    
    log_filename = 'logs.txt' if log_type == 'access' else 'message_logs.txt'
    with open(log_filename, 'a') as f:
        f.write(f"{log_entry}\n")

def get_next_registration_number():
    try:
        with open('registrations.json', 'r') as f:
            registrations = json.load(f)
            return len(registrations) + 1
    except FileNotFoundError:
        return 1

def save_registration_data(registration_data):
    try:
        with open('registrations.json', 'r') as f:
            registrations = json.load(f)
    except FileNotFoundError:
        registrations = []

    registrations.append(registration_data)

    with open('registrations.json', 'w') as f:
        json.dump(registrations, f, indent=4)

    
jututuba_history = load_chat_history_from_file('jututuba')
piht_history = load_chat_history_from_file('piht')

@app.route('/')
def index():
    return render_template('index.min.html')

@app.route('/lopupidu', methods=['GET', 'POST'])
def lopupidu():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        stay_option = request.form['stay']
        registration_data = {
            "name": full_name,
            "email": email,
            "stay": stay_option,
            "maksnud": "ei",
            "nr": get_next_registration_number()
        }
        save_registration_data(registration_data)
        return redirect(url_for('lopupidu'))
    return render_template('lopupidu.min.html')

@app.route('/lopupidu/nimekiri')
def home():
    with open('registrations.json') as f:
        data = json.load(f)
    stay_count = sum(1 for item in data if item.get('stay') == 'ööbimisega')
    return render_template('stats.min.html', data=data, total=len(data), stay_count=stay_count, json_data=json.dumps(data, indent=4))

@app.route('/lopupidu/nimekiri/edit', methods=['POST'])
def edit():
    new_data = json.loads(request.json['newData'])

    # Load old data
    with open('registrations.json') as f:
        old_data = json.load(f)

    # Compare old and new data
    with open('changes.txt', 'a') as f:
        f.write(f'\nTimestamp: {datetime.now()}\n')
        if old_data != new_data:
            f.write(f'Old data:\n{json.dumps(old_data, indent=4)}\n')
            f.write(f'New data:\n{json.dumps(new_data, indent=4)}\n')
        else:
            f.write('No changes were made.\n')

    # Save new data
    with open('registrations.json', 'w') as f:
        json.dump(new_data, f)

    return '', 200

@app.before_request
def log_request_info():
    log_request(request)

@app.before_request
def before_request():
    if app.env == "development":
        return
    if request.is_secure:
        return

    url = request.url.replace("http://", "https://", 1)
    code = 301
    return redirect(url, code=code)

@socketio.on('connect')
def handle_connect():
    global jututuba_history, piht_history
    for message in jututuba_history:
        emit('new_message', message)
    for message in piht_history:
        emit('new_message', message)

@socketio.on('send_message')
def handle_send_message(data):
    global jututuba_history, piht_history
    chatroom = data['chatroom']
    username = data['username']
    client_ip = request.remote_addr

    if chatroom == 'jututuba':
        jututuba_history.append(data)
        jututuba_history = jututuba_history[-100:]
    else:
        piht_history.append(data)
        piht_history = piht_history[-100:]
    save_message_to_file(f"{username}: {data['content']}", chatroom)
    emit('new_message', data, broadcast=True)

    logging.info(f"IP: {client_ip} | Username: {username} | Chatroom: {chatroom} | Message: {data['content']}")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=443, ssl_context=('fullchain.pem', 'privkey.pem'))