#!/usr/bin/env python3
""" Server Side
Run this file to open the server.
"""

import socket
import pickle
import json
import sys
import xmltodict

from dict2xml import dict2xml
from cryptography.fernet import Fernet
from os.path import exists as file_exists

# Key for fernet encryption
key = "R29kemlsbGFJc0p1c3RBSHVnZVRvYWRDYWxsZWRUaW0="

# Data from socket
inc_data = ""


def decrypt(token: bytes):
    """Function for decrpytion of dictionary"""
    return Fernet(key).decrypt(token)


def start_server(PORT):
    """Start up server

    Keyword arguments:
    PORT -- the desired port number eg. 5000
    """
    global inc_data
    HOST = '127.0.0.1'  # Local machine

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


def serialised_receive():
    """Receiving Serialised data"""
    # Open server
    start_server(5000)
    full_data = inc_data[2:-1].split('~')

    # Parse received data
    message = full_data[1].replace('\\\\', '\\')
    message = message.encode('utf-8')
    message = message.decode('unicode-escape').encode('latin1')

    # De-serialise data
    if (full_data[0] == "pickle"):
        dict_ = pickle.loads(message)
    if (full_data[0] == "json"):
        dict_ = json.loads(message)
    if (full_data[0] == "xml"):
        dict_ = xml_deserialise(message)

    # Output to screen or save to file
    if (full_data[2] == "1"):
        print(f"You provided the server with:\n{dict_}")
    if (full_data[2] == "2"):
        file_creator(str(dict_), "dictionary")


def xml_deserialise(message):
    """De-Serialise a Serialised XML string

    Keyword arguments:
    message -- the string to de-serialise
    """
    msg_parsed = str(message)[2:-1]
    msg_deserial = xmltodict.parse(msg_parsed)
    s_dict = msg_deserial["root"]
    try:
        s_dict.pop('#text')
        msg_dict = dict(s_dict)

        return(msg_dict)
    except KeyError:
        return(s_dict)


def file_receive():
    """Receiving File"""
    # Open server
    start_server(5050)

    full_data = inc_data[2:-1]
    plain_text = decrypt(full_data.encode('utf-8')).decode()
    decrypt_text = plain_text.split("~")

    if(decrypt_text[1] == "1"):
        print(decrypt_text[0])
    if(decrypt_text[1] == "2"):
        file_creator(decrypt_text[0], "file")


def file_creator(content, type):
    """Create file

    Keyword arguments:
    content -- content for the file as a string
    """

    file_num = 1
    while(True):
        filename = type + str(file_num) + ".txt"
        # If file exists don't write, increment number
        if(file_exists(filename) is False):
            file = open(filename, 'w+')
            file.write(content)
            file.close()
            print(f"{filename} created!")
            return True

        file_num += 1


def main():
    """ Server Main Function
    The starting point for execution for the programme.
    """
    global inc_data
    # Data from socket
    inc_data = ""

    # For testing serialised_receive()
    if len(sys.argv) > 1:
        if(sys.argv[1] == "-T"):
            for i in range(2):
                serialised_receive()
    else:
        serialised_receive()
        file_receive()


if __name__ == "__main__":
    main()
