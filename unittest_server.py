import unittest
from server import decrypt, xml_deserialize, file_creator

from client import encrypt


class TestServer(unittest.TestCase):
    def test_server(self):
        self.assertTrue(True)

    def test_decrypt_text(self):
        encrypted_text = encrypt(b"Hello World")
        decrypted_text = decrypt(encrypted_text)
        self.assertEqual(decrypted_text, b"Hello World")

    def test_file_creator(self):
        self.assertTrue(file_creator("test content"))

    def test_xml_deserialize(self):
        xml_string = b'<root><a>1</a><b>2</b></root>'
        xml_dict = xml_deserialize(xml_string)
        self.assertEqual(xml_dict, {'a': '1', 'b': '2'})


if __name__ == '__main__':
    unittest.main()
