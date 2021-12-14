"""Unittest client side

Class tests: 
1. Server test
2. Decryption test
3. File creation 
4. Xml de-serialize test
"""

import unittest
from server import decrypt, xml_deserialize, file_creator

from client import encrypt


class TestServer(unittest.TestCase):

# compare test value with true
    def test_server(self):
        self.assertTrue(True)

# test quality assesrtion to the original string
    def test_decrypt_text(self):
        encrypted_text = encrypt(b"Hello World")
        decrypted_text = decrypt(encrypted_text)
        self.assertEqual(decrypted_text, b"Hello World")

# file creation assesrtion 
    def test_file_creator(self):
        self.assertTrue(file_creator("test content"))

# test xml de-serialize function
    def test_xml_deserialize(self):
        xml_string = b'<root><a>1</a><b>2</b></root>'
        xml_dict = xml_deserialize(xml_string)
        self.assertEqual(xml_dict, {'a': '1', 'b': '2'})


if __name__ == '__main__':
    unittest.main()
