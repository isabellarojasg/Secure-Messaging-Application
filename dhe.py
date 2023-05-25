#encrypt messages using dhe
import random

global generator    # generator and prime are global because they are a constant for all users
global prime

generator = 2
prime = 23
key_length = 4

# Generates a random private key number from 1 to key_length
# Return the generated private_key
def generate_private_key():
    private_key = int(random.randint(1, key_length))
    return private_key

# Generates public key using given private_key of user
# Public key is given by: public_key = (g ^ private_key) mod p
# Return the generated public_key
def generate_public_key(private_key):
    public_key = (generator**private_key)%prime      
    return public_key

# Generates session key using generated private keys for user1 and user2.
# Session key is given by: session_key = g ^ (private_key1 * private_key2)
# Return the generated session_key
def generate_session_key(private_key1, private_key2):
    session_key = generator**(private_key1*private_key2)
    return session_key

# Encrypt the message and return it
def encrypt_message(msg, session_key):
    enc_msg = ""
    key = session_key
    for i in msg:
        enc_msg += chr(ord(i) + key)
    return enc_msg

# Decrypt the encrypted message given and return it
def decrypt_message(enc_msg, session_key):
    dec_msg = ""
    key = session_key
    for i in enc_msg:
        dec_msg += chr(ord(i) + key)
    return dec_msg
