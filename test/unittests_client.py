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

from src.client import serialize, send_data, encrypt, parse_final_data
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

    def test_serialize_json(self):
        """Assert the output of the serialize function for JSON"""
        print("[*] Testing serialize for JSON")
        self.assertEqual(
            serialize({"a": 1, "b": 2}, "2"),
            (b'{\n    "a": 1,\n    "b": 2\n}', 'json')
        )
        print("[+] Serialize for JSON passed")

    def test_serialize_xml(self):
        """Assert the output of the serialize function for XML"""
        print("[*] Testing serialize for XML")
        self.assertEqual(
            serialize({"a": 1, "b": 2}, "3"),
            (b'<root>\n<a>1</a>\n<b>2</b>\n</root>', 'xml')
        )
        print("[+] Serialize for XML passed")

    def test_serialize_pickle(self):
        """Assert the output of the serialize function for Pickle"""
        print("[*] Testing serialize for Pickle")
        self.assertEqual(
            serialize({"a": 1, "b": 2}, "1"),
            (pickle_string,
             'pickle')
        )
        print("[+] Serialize for Pickle passed")

    def test_invalid_serialize(self):
        """Test the serialization for an invalid type"""
        print("[*] Testing serialize for invalid type")
        self.assertEqual(
            serialize({"a": 1, "b": 2}, "400"),
            ('', '')
        )

    def test_send_data(self):
        """Test the send_data function"""
        print("[*] Testing send_data")

        data, method = serialize({"a": 1, "b": 2}, "2")
        self.assertEqual(
            send_data(parse_final_data(
                method=method, serialized=data, option="1"),
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
                serialized=b'{\n    "a": 1,\n    "b": 2\n}'
            ),
            "json" + '~' +
            str(b'{\n    "a": 1,\n    "b": 2\n}')[2:-1] + '~' + str("1")
        )
        print("[+] parse_final_data passed")

if __name__ == '__main__':
    unittest.main()
