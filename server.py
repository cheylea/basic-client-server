# Steps #
## Open and listen on port XXXX
## Process socket data
## Split string into sections
## process serialization
## Print or send to file
## Open and listen on port XXXX
## process socket data
## process encrypted file
## print file contents



import socket
import pickle
import json 
import sys

from dict2xml import dict2xml
from cryptography.fernet import Fernet
import xmltodict
from os.path import exists as file_exists


# Key for fernet encryption
key = "R29kemlsbGFJc0p1c3RBSHVnZVRvYWRDYWxsZWRUaW0="

# Data from socket
inc_data = ""

# Function for decrpytion of dictionary
def decrypt(token: bytes):
    return Fernet(key).decrypt(token)


def start_server(PORT):
    global inc_data
    # Start up server
    HOST = '127.0.0.1' # Local machine

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, PORT))
        except:
            print(f"Unable to bind to {HOST}:{PORT}")
            sys.exit(1)
        print(f"Server Open on {HOST}:{PORT}")
        s.listen()
        s.settimeout(30)
        conn, addr = s.accept()
        with conn:
            print(f"{addr[0]} Connected")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)
                inc_data = repr(data)




### Expecting Serialization data ####
start_server(1337)

full_data = inc_data[2:-1].split('~')


if (full_data[0] == 'y'): 
    message = decrypt(full_data[1].encode('utf-8'))
else:
    message = full_data[1].replace('\\\\', '\\')
    message = message.encode('utf-8')
    message = message.decode('unicode-escape').encode('latin1')    
    

def xml_deserialize(message):
    msg_parsed = str(message)[2:-1]
    msg_deserial = xmltodict.parse(msg_parsed)
    s_dict = msg_deserial["root"]
    s_dict.pop('#text')
    msg_dict = dict(s_dict)

    return(msg_dict)
    

# De-serialize
if (full_data[0] == "pickle"): dict = pickle.loads(message)
if (full_data[0] == "json"): dict = json.loads(message)
if (full_data[0] == "xml"): dict = xml_deserialize(message); 


def file_creator(content):
    # If file exists don't write, increment number
    found = False
    file_num = 1
    filename = ""
    filename = "file" + str(file_num) + ".txt"
    found = file_exists(filename)
    
    while(True):    
        filename = "file" + str(file_num) + ".txt"
        if(file_exists(filename) == False):
            file = open(filename,'w+')
            file.write(content)
            file.close()
            print(f"{filename} created!")
            break
                
        file_num += 1   
    
    
    
    
    
# Output to screen
if (full_data[2] == "1"): print(f"You provided the server with:\n{dict}")
if (full_data[2] == "2"): file_creator(str(dict))



### Expecting File ###
start_server(13373)

full_data = inc_data[2:-1]
decrypt_text = decrypt(full_data.encode('utf-8')).decode()
print(decrypt_text)
