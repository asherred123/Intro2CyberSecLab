import random
import argparse

def dhke_setup(nb):
    return (1208925819614629174706189, 3 )

def gen_priv_key(p):
    key = random.randrange(2, p)
    return key 

def get_pub_key(alpha, a, p):
    key = pow(alpha, a, p)
    return key 

# constants
FULLROUND = 31

# S-Box Layer
sbox = [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD,
        0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]

# PLayer
pmt = [0, 16, 32, 48, 1, 17, 33, 49, 2, 18, 34, 50, 3, 19, 35, 51,
       4, 20, 36, 52, 5, 21, 37, 53, 6, 22, 38, 54, 7, 23, 39, 55,
       8, 24, 40, 56, 9, 25, 41, 57, 10, 26, 42, 58, 11, 27, 43, 59,
       12, 28, 44, 60, 13, 29, 45, 61, 14, 30, 46, 62, 15, 31, 47, 63]

# Rotate left: 0b1001 --> 0b0011
inv_sbox = [sbox.index(i) for i in range(16)]

def inv_sBoxLayer(state):
    new_state = 0
    for i in range(16):
        nibble = (state >> (i * 4)) & 0xF
        substituted = inv_sbox[nibble]
        new_state |= (substituted << (i * 4))
    return new_state

def inv_pLayer(state):
    output = 0x0000000000000000
    for i in range(64):
        bit = (state >> pmt[i]) & 0x1
        output |= bit << i
    return output

def rol(val, r_bits, max_bits): 
    return (val << r_bits % max_bits) & (2**max_bits - 1) | ((val & (2**max_bits - 1)) >> (max_bits - (r_bits % max_bits)))

def ror(val, r_bits, max_bits):
    return ((val & (2**max_bits - 1)) >> r_bits % max_bits) | (val << (max_bits - (r_bits % max_bits)) & (2**max_bits - 1))

def genRoundKeys(key):
    """Generate round keys for all rounds."""
    round_keys = {}
    round_keys[0] = 32
    for round_counter in range(1, FULLROUND + 2):
        round_key = (key >> 16) & 0xFFFFFFFFFFFFFFFF
        round_keys[round_counter] = round_key
        key = rol(key, 61, 80)
        top_four_bits = (key >> 76) & 0xF
        substituted = sbox[top_four_bits]
        key = (key & ~(0xF << 76)) | (substituted << 76)
        key = key ^ (round_counter << 15)
    return round_keys

def addRoundKey(state, Ki):
    state = state ^ Ki
    return state

def sBoxLayer(state):
    new_state = 0
    for i in range(16):
        nibble = (state >> (i * 4)) & 0xF
        substituted = sbox[nibble]
        new_state |= (substituted << (i * 4))
    return new_state

def pLayer(state):
    output = 0x0000000000000000
    for i in range(64):
        bit = (state >> i) & 0x1
        output |= bit << pmt[i]
    return output

def present_round(state, roundKey):
    state = addRoundKey(state, roundKey)
    state = sBoxLayer(state)
    state = pLayer(state)
    return state

def present_inv_round(state, roundKey):
    state = inv_pLayer(state)
    state = inv_sBoxLayer(state)
    state = addRoundKey(state, roundKey)
    return state

def present(plain, key):
    K = genRoundKeys(key)
    state = plain
    for i in range(1, FULLROUND + 1):
        state = present_round(state, K[i])
    state = addRoundKey(state, K[32])
    return state

def present_inv(cipher, key):
    K = genRoundKeys(key)
    state = cipher
    state = addRoundKey(state, K[32])
    for i in range(FULLROUND, 0, -1):
        state = present_inv_round(state, K[i])
    return state

def get_shared_key(keypub, keypriv, p):
    key = pow(keypub, keypriv, p)
    return key 

nokeybits = 80
blocksize = 64

def pad(data):
    pad_len = 8 - (len(data) % 8)
    return data + bytes([pad_len] * pad_len)

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

def ecb_encrypt(plaintext, key):
    plaintext = pad(plaintext)
    ciphertext = bytearray()
    for i in range(0, len(plaintext), 8):
        block = int.from_bytes(plaintext[i:i+8], byteorder='big')
        encrypted_block = present(block, key)
        ciphertext.extend(encrypted_block.to_bytes(8, byteorder='big'))
    return ciphertext

def ecb_decrypt(ciphertext, key):
    plaintext = bytearray()
    for i in range(0, len(ciphertext), 8):
        block = int.from_bytes(ciphertext[i:i+8], byteorder='big')
        decrypted_block = present_inv(block, key)
        plaintext.extend(decrypted_block.to_bytes(8, byteorder='big'))
    return unpad(plaintext)
       
if __name__ == "__main__":
    p, alpha = dhke_setup(80)
    print("Generate P and alpha:")
    print("P:", p)
    print("alpha:", alpha)
    print()
    a = gen_priv_key(p)
    b = gen_priv_key(p)
    print("My private key is: ", a)
    print("Test other private key is: ", b)
    print()
    A = get_pub_key(alpha, a, p)
    B = get_pub_key(alpha, b, p)
    print("My public key is: ", A)
    print("Test other public key is: ", B)
    print()
    sharedKeyA = get_shared_key(B, a, p)
    sharedKeyB = get_shared_key(A, b, p)
    print("My shared key is: ", sharedKeyA)
    print("Test other shared key is: ", sharedKeyB)
    print("Length of key is %d bits." % sharedKeyA.bit_length())

    plaintext = "hello from A"
    print("Plaintext:", plaintext)
    plaintext_bytes = plaintext.encode()
    
    cipher = ecb_encrypt(plaintext_bytes, sharedKeyA)
    print("Ciphertext:", cipher)
    
    decrypted_bytes = ecb_decrypt(cipher, sharedKeyB)
    decrypted_text = decrypted_bytes.decode()
    
    print("Decrypted text:", decrypted_text)
    print("plaintext == decrypted_text:",
plaintext == decrypted_text)
