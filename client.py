"""Client Side

Steps:
1. Check server connection open
2. Choose serializiation type / output
3. Send data
4. Choose file
5. Choose if saved locally
6. Send data
"""

import socket
import pickle
import json

from dict2xml import dict2xml

from cryptography.fernet import Fernet

# Key for fernet encryption
key = "R29kemlsbGFJc0p1c3RBSHVnZVRvYWRDYWxsZWRUaW0="

default_dict = {}

# Functions for encrpytion of dictionary
def encrypt(message: bytes):
    return Fernet(key).encrypt(message)


# Send data to server
def send_data(serialized_data, PORT):
    HOST = '127.0.0.1'  # Local machine

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(serialized_data.encode('latin1'))
        data = s.recv(1024)

def dict_enter():
    global default_dict
    value_amounts = input("### How many values do you want to use? ###\n")
    for v in range(int(value_amounts)):
        dict_key = input("### Enter a key ###\n")
        dict_value = input("### Enter a value ###\n")
        default_dict[dict_key] = dict_value
        

# Whole Structure to query user
def serialize(default_dict, s_type):
    # Serialize data
    serialized = ""
    method = ""
    if(s_type == '1'):
        serialized = pickle.dumps(default_dict)
        method = "pickle"
    if(s_type == '2'):
        serialized = json.dumps(
            default_dict, sort_keys=True, indent=4).encode()
        method = "json"
    if(s_type == '3'):
        serialized = dict2xml(default_dict, wrap='root', indent="").encode()
        method = "xml"
    return serialized, method


def parse_final_data(method, serialized, option):
    return method + '~' + str(serialized)[2:-1] + '~' + str(option)


def main():
    global default_dict
    """Serialize Section"""
    
    # Dictionary to send
    d_type = input("### Do you wish to manually enter a dictionary? (Y) (N) ###\n")
    if(d_type.lower() == "y"):
        dict_enter()
    else:
        default_dict = {"mykey": "myvalue", "yourkey": "yourvalue"}
        
    # Chose serialization type
    s_type = input("### Please Choose Serialization Type ###"
                   "\n### Pickle Binary (1), Json (2), XML (3) ###\n")

    # Output to screen or file
    option = input("### Do you want to output "
                   "to the screen (1) or file (2) ###\n").lower()

    # Append to data for later review, seperated by ~
    # Method~Serialized~Print/File
    # e.g. json~{\n    "mykey": "myvalue",\n    "yourkey": "yourvalue"\n}~1

    serialized, method = serialize(default_dict, s_type)

    final_data = parse_final_data(method, serialized, option)

    # Send data to server
    send_data(final_data, 5000)
    print("### Your data has been sent to ###")

    """File Section"""
    # File choice and encrpytion
    file_choice = input("\n\n### Please Choose enter your filename that includes .txt ###\n")
    enc_file_choice = input("### Do you wish to locally encrypt your file?"
                            "(Y) (N) ###\n").lower()

    # Take in a read file
    f = open(file_choice, "r")
    file_contents = ""
    for line in f:
        file_contents += line
    
    # Encrypt file contents (.txt files only contain text)
    enc_file_content = encrypt(file_contents.encode())
    
    # Save encrypted version to disc
    if(enc_file_choice == "y"):

        # Create encrypted file name XXXX_enc.txt
        split_name = file_choice.split(".")
        enc_file_name = split_name[0] + "_enc.txt"

        # Create file
        file = open(enc_file_name, 'w')
        file.write(enc_file_content.decode())
        file.close()
        print(f"{enc_file_name} created!")
        
    send_data(enc_file_content.decode(), 5050)




if __name__ == "__main__":
    main()

