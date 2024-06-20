#!/usr/bin/env python3
# ECB plaintext extraction skeleton file for 50.042 FCS

from collections import Counter
import argparse

def getInfo(headerfile):
    with open(headerfile, 'rb') as f:
        header = f.read()
        print(header, len(header))
    return len(header), header

def extract(infile, outfile, headerfile):
    header_length, header = getInfo(headerfile)
    block_list = []

    # Read the input file
    with open(infile, 'rb') as f:
        data = f.read()
    
    # Ignore header
    data = data[header_length:]

    # Read data in 8-byte blocks and append to list
    for i in range(0, len(data), 8):
        block = data[i:i+8]
        block_list.append(block)
    
    # Frequency analysis
    frequency = Counter(block_list)
    most_frequent_block = max(frequency, key=frequency.get)

    # Decrypt the data based on frequency
    decrypted = []
    for block in block_list:
        if block == most_frequent_block:
            decrypted.append(b'0'*8)
        else:
            decrypted.append(b'1'*8)

    # Join the decrypted blocks
    decrypted_text = b''.join(decrypted)

    # Write the output file
    with open(outfile, 'wb') as fout:
        fout.write(header)  # Include header to ensure correct format
     
        fout.write(decrypted_text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract PBM pattern.')
    parser.add_argument('-i', dest='infile', help='input file, PBM encrypted format')
    parser.add_argument('-o', dest='outfile', help='output PBM file')
    parser.add_argument('-hh', dest='headerfile', help='known header file')

    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile
    headerfile = args.headerfile

    print('Reading from: %s' % infile)
    print('Reading header file from: %s' % headerfile)
    print('Writing to: %s' % outfile)

    extract(infile, outfile, headerfile)
