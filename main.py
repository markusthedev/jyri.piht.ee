input_file = 'server_logs.txt'   # Replace 'input.txt' with the path to your text file
output_file = 'output.txt' # Replace 'output.txt' with the path to the cleaned text file
ip_to_remove = '185.244.101.83' # Replace '123.123.123.123' with the IP address you want to remove

with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        if ip_to_remove not in line:
            outfile.write(line)

# If you want to replace the original file with the cleaned file, uncomment the following lines:
import os
os.remove(input_file)
os.rename(output_file, input_file)
