from cryptography.fernet import Fernet


class Hasher:
    """
    Class for hashing tokens in database
    """
    def __init__(self, key: str):
        """
        Create the hasher object with custom key
        :param key: value for hashing
        """
        self.f = Fernet(str.encode(key))

    @staticmethod
    def generate_key(filepath='secret.key') -> None:
        """
        Method that generates key and writes into file
        :param filepath: path to file
        :return: nothing to return
        """
        key = Fernet.generate_key()
        with open(filepath, 'wb') as key_file:
            key_file.write(key)

    @staticmethod
    def load_key(filepath='secret.key') -> bytes:
        """
        Method that gets pre-generated key from file
        :param filepath: path to file
        :return: key in bytes format
        """
        return open(filepath, 'rb').read()

    def encrypt_message(self, message: str) -> bytes:
        """
        Method that encrypts string into hashing string
        :param message: message to encrypt
        :return: encrypted string
        """
        encoded_message = message.encode('utf-8')
        try:
            encrypted_message = self.f.encrypt(encoded_message)
        except TypeError:
            return b''
        return encrypted_message

    def decrypt_message(self, encrypted_message: bytes) -> str:
        """
        Method that decrypts hashing string into string
        :param encrypted_message: hashing string
        :return: decrypted string
        """
        try:
            decrypted_message = self.f.decrypt(encrypted_message).decode()
        except TypeError:
            return ''
        return decrypted_message
