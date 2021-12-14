""" Unittests for client side

Unit tests: 
1. Server connection
2. Json serialization
3. XML serialization
4. Pickle serialization
5. Invalid serialization
6. Data submission
7. Encryption process
8. Parse parameter
"""

import unittest
from client import serialize, send_data, encrypt, parse_final_data
import socket

import time

class TestClient(unittest.TestCase):

# Test whether server is active
    def test_server_active(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect(("127.0.0.1", 5000))
                self.assertTrue(True)
                print("[+] Server is active")
                s.close()
            except ConnectionRefusedError:
                self.assertTrue(False)
                print("[-] Server is not active")

# Asserting the output of the serialize function for JSON    
    def test_serialize_json(self):
        print("[*] Testing serialize for JSON")
        self.assertEqual(
            serialize({"a": 1, "b": 2}, "2"),
            (b'{\n    "a": 1,\n    "b": 2\n}', 'json')
        )
        print("[+] Serialize for JSON passed")

# Asserting the output of the serialize function for XML 
    def test_serialize_xml(self):
        print("[*] Testing serialize for XML")
        self.assertEqual(
            serialize({"a": 1, "b": 2}, "3"),
            (b'<root>\n<a>1</a>\n<b>2</b>\n</root>', 'xml')
        )
        print("[+] Serialize for XML passed")

# Asserting the output of the serialize function for Pickle  
    def test_serialize_pickle(self):
        print("[*] Testing serialize for Pickle")
        self.assertEqual(
            serialize({"a": 1, "b": 2}, "1"),
            (b'\x80\x04\x95\x11\x00\x00\x00\x00\x00\x00\x00}\x94(\x8c\x01a\x94K\x01\x8c\x01b\x94K\x02u.', 'pickle')
        )
        print("[+] Serialize for Pickle passed")

# Invalid type serialization test
    def test_invalid_serialize(self):
        print("[*] Testing serialize for invalid type")
        self.assertEqual(
            serialize({"a": 1, "b": 2}, "400"),
            ('', '')
        )
# Test send data function 
    def test_send_data(self):
        print("[*] Testing send_data")

        data, method = serialize({"a": 1, "b": 2}, "2")
        self.assertEqual(
            send_data(parse_final_data(
                method=method, serialized=data, option="1"),
                    5000),
                        None)
        print("[+] send_data passed")

# Perform enryption test
    def test_encrypt(self):
        print("[*] Testing encrypt")
        self.assertTrue(
            encrypt(b'a secret message') != None
        )
        print("[+] encrypt passed")

# Passing final data to tests the respective function 
    def test_parse_final_data(self):
        print("[*] Testing parse_final_data")
        self.assertEqual(
            parse_final_data(
                method="json", option="1", serialized=b'{\n    "a": 1,\n    "b": 2\n}'
            ),
            "json" + '~' +
            str(b'{\n    "a": 1,\n    "b": 2\n}')[2:-1] + '~' + str("1")
        )
        print("[+] parse_final_data passed")


if __name__ == '__main__':
    unittest.main()
