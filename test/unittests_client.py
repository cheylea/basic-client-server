#!/usr/bin/env python3
"""Client Side Unit Tests
This file contains a unit testing class for testing the functionality
of src/client.py.
"""

import unittest
import os
import inspect
import sys
import socket

cdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(cdir)
sys.path.insert(0, parentdir)

from src.client import serialise, send_data, encrypt, parse_final_data
from src.server import decrypt


pickle_string = (
                 '\x80\x04\x95\x11\x00\x00\x00\x00' +
                 '\x00\x00\x00}\x94(\x8c\x01a\x94K' +
                 '\x01\x8c\x01b\x94K\x02u.'
            ).encode("latin1")


class TestClient(unittest.TestCase):
    """ Client Side Unit Tests"""

    def test_server_active(self):
        """Test whether the server is active"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect(("127.0.0.1", 5000))
                self.assertTrue(True)
                print("[+] Server is active")
                s.close()
            except ConnectionRefusedError:
                self.assertTrue(False)
                print("[-] Server is not active")

    def test_serialise_json(self):
        """Assert the output of the serialise function for JSON"""
        print("[*] Testing serialise for JSON")
        self.assertEqual(
            serialise({"a": 1, "b": 2}, "2"),
            (b'{\n    "a": 1,\n    "b": 2\n}', 'json')
        )
        print("[+] Serialise for JSON passed")

    def test_serialise_xml(self):
        """Assert the output of the serialise function for XML"""
        print("[*] Testing serialise for XML")
        self.assertEqual(
            serialise({"a": 1, "b": 2}, "3"),
            (b'<root>\n<a>1</a>\n<b>2</b>\n</root>', 'xml')
        )
        print("[+] Serialise for XML passed")

    def test_serialise_pickle(self):
        """Assert the output of the serialise function for Pickle"""
        print("[*] Testing serialise for Pickle")
        self.assertEqual(
            serialise({"a": 1, "b": 2}, "1"),
            (pickle_string,
             'pickle')
        )
        print("[+] Serialise for Pickle passed")

    def test_invalid_serialise(self):
        """Test the serialisation for an invalid type"""
        print("[*] Testing serialise for invalid type")
        self.assertEqual(
            serialise({"a": 1, "b": 2}, "400"),
            ('', '')
        )

    def test_send_data(self):
        """Test the send_data function"""
        print("[*] Testing send_data")

        data, method = serialise({"a": 1, "b": 2}, "2")
        self.assertEqual(
            send_data(parse_final_data(
                method=method, serialised=data, option="1"),
                    5000), "Data Sent")
        print("[+] send_data passed")

    def test_encrypt(self):
        """Test the encrypt function"""
        print("[*] Testing encrypt")
        encrypt_string = encrypt(b'a secret message')
        self.assertEqual(
            decrypt(encrypt_string), b'a secret message'
            )

        print("[+] encrypt passed")

    def test_parse_final_data(self):
        """Test the the final data format"""
        print("[*] Testing parse_final_data")
        self.assertEqual(
            parse_final_data(
                method="json", option="1",
                serialised=b'{\n    "a": 1,\n    "b": 2\n}'
            ),
            "json" + '~' +
            str(b'{\n    "a": 1,\n    "b": 2\n}')[2:-1] + '~' + str("1")
        )
        print("[+] parse_final_data passed")

if __name__ == '__main__':
    unittest.main()
