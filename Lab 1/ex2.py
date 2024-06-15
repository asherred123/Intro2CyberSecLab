 #!/usr/bin/env python3
# SUTD 50.042 FCS Lab 1
# Simple file read in/out


# Import libraries
import sys
import argparse
import string

def doStuff(filein, fileout, k , m):
    # open file handles tdo both files
    fin = open(filein, mode="r", encoding="utf-8", newline="\n")  # read mode
    fin_b = open(filein, mode="rb")  # binary read mode
    fout = open(fileout, mode="w", encoding="utf-8", newline="\n")  # write mode
    fout_b = open(fileout, mode="wb")  # binary write mode
    
    # and write to fileout

    # close all file streams
    fin.close()
    fin_b.close()
    fout.close()
    fout_b.close()

    # PROTIP: pythonic way
    with open(filein, mode="rb") as fin:
    # read the file as a sequence of bytes
        byte_arr = bytearray(fin.read())    
    #convert k to bytes
    k = k.to_bytes(1, byteorder='big')

    if m == 'e':
        # for encryption, add the key to byte_arr
        byte_arr = bytearray([(b + k[0]) % 256 for b in byte_arr])
    elif m == 'd':
        # for decryption, subtract the key from each byte
        byte_arr = bytearray([(b - k[0]) % 256 for b in byte_arr])

# open the output file in binary mode
    with open(fileout, mode="wb") as fout:
    # write the modified bytes to the file
     fout.write(byte_arr)
    


        # file will be closed automatically when interpreter reaches end of the block


# our main function
if __name__ == "__main__":
    # set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="filein", help="input file")
    parser.add_argument("-o", dest="fileout", help="output file")
    parser.add_argument("-k" , dest="key",type = int,  help="key for encryption")

    parser.add_argument("-m" , dest="mode", help="mode of encryption")
    # parse our arguments
    args = parser.parse_args()
    filein = args.filein
    fileout = args.fileout
    k = args.key
    m = args.mode 
    # check if key is within the valid range
    if not (1 <= k <= 255):
        print("Error: The key must be between 1 and 255")
        exit(1)

    doStuff(filein, fileout, k , m )

    # all done
