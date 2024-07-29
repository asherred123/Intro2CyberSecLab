from Crypto.PublicKey import RSA 
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import pss
import base64
import random

def generate_RSA(bits=1024):
    key = RSA.generate(bits)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

# Save the keys to files
private_key, public_key = generate_RSA()
with open("private_key_file.pem", "wb") as prv_file:
    prv_file.write(private_key)

with open("public_key_file.pem", "wb") as pub_file:
    pub_file.write(public_key)

def encrypt_RSA(public_key_file, message):
    with open(public_key_file, "rb") as pub_file:
        public_key = RSA.import_key(pub_file.read())
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_message = cipher.encrypt(message.encode())
    return base64.b64encode(encrypted_message).decode()

message = "This is a secret message."
ciphertext = encrypt_RSA("public_key_file.pem", message)
print("Ciphertext:", ciphertext)

def decrypt_RSA(private_key_file, ciphertext):
    with open(private_key_file, "rb") as prv_file:
        private_key = RSA.import_key(prv_file.read())
    cipher = PKCS1_OAEP.new(private_key)
    decrypted_message = cipher.decrypt(base64.b64decode(ciphertext))
    return decrypted_message.decode()

decrypted_message = decrypt_RSA("private_key_file.pem", ciphertext)
print("Decrypted message:", decrypted_message)

def sign_data(private_key_file, data):
    with open(private_key_file, "rb") as prv_file:
        private_key = RSA.import_key(prv_file.read())
    hash = SHA256.new(data.encode())
    signature = pss.new(private_key).sign(hash)
    return base64.b64encode(signature).decode()

signature = sign_data("private_key_file.pem", message)
print("Signature:", signature)

def verify_sign(public_key_file, sign, data):
    with open(public_key_file, "rb") as pub_file:
        public_key = RSA.import_key(pub_file.read())
    hash = SHA256.new(data.encode())
    try:
        pss.new(public_key).verify(hash, base64.b64decode(sign))
        print("The signature is valid.")
        return True
    except (ValueError, TypeError):
        print("The signature is not valid.")
        return False

verification = verify_sign("public_key_file.pem", signature, message)
print("Verification result:", verification)

def perform_attack(public_key_file):
    with open(public_key_file, "rb") as pub_file:
        public_key = RSA.import_key(pub_file.read())
    
    s = random.getrandbits(1024)  
    x = pow(s, public_key.e, public_key.n)  # Compute x = s^e mod n

    return s, x

# 2. Verify the forged signature
def verify_forged_signature(public_key_file, s, x):
    with open(public_key_file, "rb") as pub_file:
        public_key = RSA.import_key(pub_file.read())
    
    x_bytes = x.to_bytes((x.bit_length() + 7) // 8, byteorder='big')
    s_bytes = s.to_bytes((s.bit_length() + 7) // 8, byteorder='big')
    
    try:
        pss.new(public_key).verify(SHA256.new(x_bytes), s_bytes)
        print("Attack Suceeded.")
    except (ValueError, TypeError):
        print("Attack Failed.")

# Perform the attack
s, x = perform_attack("public_key_file.pem")
verify_forged_signature("public_key_file.pem", s, x)