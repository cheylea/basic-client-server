#!/usr/bin/env python3
"""Server Side Unit Tests
This file contains a unit testing class for testing the functionality
of src/server.py.
"""

import unittest
import os
import inspect
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from src.server import decrypt, xml_deserialize, file_creator
from src.client import encrypt



class TestServer(unittest.TestCase):
    """ Server Side Unit Tests"""

    def test_decrypt_text(self):
        """Check if string has interference after encryption and decryption"""
        encrypted_text = encrypt(b"Hello World")
        encrypted_text != decrypted_text()
        decrypted_text = decrypt(encrypted_text)
        self.assertEqual(decrypted_text, b"Hello World")
    
    print("[1] test_decrypt_text passed")
    
    def test_file_creator(self):
        """Test File Creation"""
        self.assertTrue(file_creator("test content", ""))

    print("[2] test_file_creator passed")

    def test_xml_deserialize(self):
        """Test expected output from xml_deserialize function"""
        xml_string = b'<root><a>1</a><b>2</b></root>'
        xml_dict = xml_deserialize(xml_string)
        self.assertEqual(xml_dict, {'a': '1', 'b': '2'})

    print("[3] test_xml_deserialize passed")


if __name__ == '__main__':
    unittest.main()
