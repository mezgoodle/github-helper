import os

from cryptography.fernet import Fernet


class Hasher:
    def __init__(self):
        self.f = Fernet(bytes(os.getenv('KEY', b'Kt7ioOW4eugqDkfqcYiCz2mOuyiWRg_MTzckxEVp978=')))

    @staticmethod
    def generate_key(filepath='secret.key'):
        key = Fernet.generate_key()
        with open(filepath, 'wb') as key_file:
            key_file.write(key)

    @staticmethod
    def load_key(filepath='secret.key'):
        return open(filepath, 'rb').read()

    def encrypt_message(self, message: str) -> bytes:
        encoded_message = message.encode('utf-8')
        encrypted_message = self.f.encrypt(encoded_message)
        return encrypted_message

    def decrypt_message(self, encrypted_message: bytes) -> str:
        decrypted_message = self.f.decrypt(encrypted_message).decode()
        return decrypted_message


hasher = Hasher()
print(hasher.encrypt_message('hello'))
print(hasher.decrypt_message(hasher.encrypt_message('hello')))
