#!/usr/bin/env python3
# ECB wrapper skeleton file for 50.042 FCS

from present import *
import argparse

nokeybits = 80
blocksize = 64

def pad(data):
    pad_len = 8 - (len(data) % 8)
    return data + bytes([pad_len] * pad_len)

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

def ecb(infile, outfile, keyfile, mode):
    with open(infile, 'rb') as f:
        data = f.read()
    with open(keyfile, 'r') as f:
        key = int(f.read().strip(), 16)
    
    if mode == 'encrypt':
        
        data = pad(data)
        plaintext = bytearray(data)
        ciphertext = bytearray()
        for i in range(0, len(plaintext), 8):
            block = int.from_bytes(plaintext[i:i+8], byteorder='big')
            encrypted_block = present(block, key)
            ciphertext.extend(encrypted_block.to_bytes(8, byteorder='big'))
        with open(outfile, 'wb') as f:
            f.write(ciphertext)

    elif mode == 'decrypt':
        
        ciphertext = bytearray(data)
        plaintext = bytearray()
        for i in range(0, len(ciphertext), 8):
            block = int.from_bytes(ciphertext[i:i+8], byteorder='big')
            decrypted_block = present_inv(block, key)
            plaintext.extend(decrypted_block.to_bytes(8, byteorder='big'))
        plaintext = unpad(plaintext)
        with open(outfile, 'wb') as f:
            f.write(plaintext)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Block cipher using ECB mode.')
    parser.add_argument('-i', dest='infile', help='input file')
    parser.add_argument('-o', dest='outfile', help='output file')
    parser.add_argument('-k', dest='keyfile', help='key file')
    parser.add_argument('-m', dest='mode', choices=['encrypt', 'decrypt'], help='mode')
    
    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile
    keyfile = args.keyfile
    mode = args.mode
    
    ecb(infile, outfile, keyfile, mode)
