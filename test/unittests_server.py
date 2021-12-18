#!/usr/bin/env python3
"""Server Side Unit Tests
This file contains a unit testing class for testing the functionality
of src/server.py.
"""

import unittest
import os
import inspect
import sys
cdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(cdir)
sys.path.insert(0, parentdir)

from src.server import decrypt, xml_deserialize, file_creator
from src.client import encrypt


class TestServer(unittest.TestCase):
    """Server Side Unit Tests"""

    def test_encrypt_text(self):
        """Check encryption alters string"""
        encrypted_text = encrypt(b"Hello World")
        self.assertNotEqual(encrypted_text, b"Hello World")

    def test_decrypt_text(self):
        """Check if string has interference after encryption and decryption"""
        encrypted_text = encrypt(b"Hello World")
        decrypted_text = decrypt(encrypted_text)
        self.assertEqual(decrypted_text, b"Hello World")

    def test_file_creator(self):
        """Test File Creation"""
        self.assertTrue(file_creator("test content", ""))

    def test_xml_deserialize(self):
        """Test expected output from xml_deserialize function"""
        xml_string = b'<root><a>1</a><b>2</b></root>'
        xml_dict = xml_deserialize(xml_string)
        self.assertEqual(xml_dict, {'a': '1', 'b': '2'})


if __name__ == '__main__':
    unittest.main()
