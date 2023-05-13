# jyri.piht.ee
Lehekülg kus saad hostida enda "pihti". Lisaks on siin ka registreerimisvorm, mis võimaldab kasutajatel registreeruda üritusele ja vaadata registreerunute nimekirja. Registreerimisvorm salvestab kasutaja nime, e-posti aadressi ja ööbimissoovi. Veebirakendus on loodud Pythoni veebiraamistikuga Flask ja kasutab Socket.IO teeki reaalajas suhtluseks.

## Rakenduse hostimine

1. Paigalda Python. Rakendus on testitud Pythoni versiooniga 3.8, aga peaks töötama ka uuemate versioonidega.

2. Kloonige see repo oma arvutisse:

    ```
    git clone https://github.com/markusthedev/jyri.piht.ee
    ```

3. Navigeerige repo kausta:

    ```
    cd jyri.piht.ee
    ```

4. Paigalda vajalikud teegid:

    ```
    pip install -r requirements.txt
    ```

5. Loo `.env` fail ja täida see järgmise sisuga:

    ```
    SECRET_KEY=your_secret_key
    ```

    Asenda `your_secret_key` oma Flaski rakenduse salajase võtmega.

6. Käivita rakendus:

    ```
    python server.py
    ```
