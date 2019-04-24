# -*- coding: utf-8 -*-
from Crypto.PublicKey import *
from Crypto.Hash import *
from Crypto.Signature import *
ENCRYPTION_PARAMETER = 32


class EncryptionSet(object):
    def __init__(self, private_key):
        """
        constructor
        """
        self.private_key = private_key
        self.public_key = private_key.publickey()

    @staticmethod
    def encrypt(recipient_public_key, message):
        """
        the function encrypts the message with
        the private key
        :param recipient_public_key: the public key
        of the recipient
        :param message: the message to encrypt
        :returns: the encrypted message
        """
        return recipient_public_key.encrypt(
            message,
            ENCRYPTION_PARAMETER)[0]

    def sign(self, hash_code):
        """
        the function signs the message
        using the private key
        :param hash_code: the hash code to sign
        :return: the signature that created from
        the key and the message
        """
        signer = PKCS1_v1_5.new(self.private_key)
        return signer.sign(hash_code)

    def decrypt(self, encrypted_message):
        """
        the function decrypts the
        encrypted message
        :param encrypted_message: the encrypted
        message
        :returns: the decrypted message
        """
        return self.private_key.decrypt(encrypted_message)

    @staticmethod
    def verify(hash_code, signature, sender_public_key):
        """
        verify the authenticity of the signature
        :param hash_code: the hash, that supposed to
        be the hash that the signature is signed on
        :param signature: the signature
        :param sender_public_key: the sender's public
        key
        :returns: true if he signature is authentic
        and false otherwise
        """
        verifier = PKCS1_v1_5.new(sender_public_key)
        return verifier.verify(hash_code, signature)

    @staticmethod
    def hash(message):
        """
        the function hashes the message and returns
        the hash code
        :param message: the message to hash
        :returns: the hash code
        """
        return SHA256.new(message)


if __name__ == '__main__':
    private_key_1 = RSA.generate(2048)
    encryption_set_1 = EncryptionSet(private_key_1)
    private_key_2 = RSA.generate(2048)
    encryption_set_2 = EncryptionSet(private_key_2)
    message_to_encrypt = 'try to encrypt'
    assert_encrypt_message = encryption_set_1.encrypt(
        encryption_set_2.public_key,
        message_to_encrypt)
    decrypted_message = encryption_set_2.decrypt(assert_encrypt_message)
    assert decrypted_message == message_to_encrypt
    decrypted_message = encryption_set_1.decrypt(assert_encrypt_message)
    assert decrypted_message != message_to_encrypt
    assert_hash_code = encryption_set_1.hash(message_to_encrypt)
    assert_signature = encryption_set_1.sign(assert_hash_code)
    assert encryption_set_2.verify(
        assert_hash_code,
        assert_signature,
        encryption_set_1.public_key)