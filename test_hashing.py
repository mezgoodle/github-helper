from unittest import TestCase

from hashing import Hasher


class TestHasher(TestCase):
    def setUp(self):
        self.hasher = Hasher()
        self.message = 'Test message'

    def test_generate_and_load_key(self):
        self.hasher.generate_key()
        key = self.hasher.load_key()
        self.assertIsNotNone(key)
        self.assertIsInstance(key, bytes)

    def test_encrypt_message(self):
        encrypted_message = self.hasher.encrypt_message(self.message)
        self.assertIsNotNone(encrypted_message)
        self.assertIsInstance(encrypted_message, bytes)

    def test_decrypt_message(self):
        encrypted_message = self.hasher.encrypt_message(self.message)
        decrypted_message = self.hasher.decrypt_message(encrypted_message)
        self.assertIsNotNone(decrypted_message)
        self.assertIsInstance(decrypted_message, str)
        self.assertEqual(decrypted_message, self.message)
