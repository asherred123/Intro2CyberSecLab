from Crypto.PublicKey import RSA 
from Crypto.Hash import SHA256
#encrypt message.txt using RSA using public key mykey.pem.pub 

key = open('Lab 7/mykey.pem.pub','r').read() 
rsakey = RSA.importKey(key) # public key 
key = open('Lab 7/mykey.pem.priv','r').read() 
rsakey = RSA.importKey(key) # private key 
# private key 



def square_multiply(a,x,n):
    
    y = 1
    n_b = int(x.bit_length())
    for i in range(n_b,-1,-1):
        y = y**2%n
        if x &(1<<i):
            y = a*y%n
    return y


def encrypt(message): 
    message_bytes = message.encode("utf-8")  #convert from string the bytes
    message_int = int.from_bytes(message_bytes, byteorder= 'big') #convert bytes to int 
    m  = square_multiply(message_int,  rsakey.e, rsakey.n)

    return m 

def decrypt(cipher_text): 
    m = square_multiply(cipher_text , rsakey.d , rsakey.n)
    message_bytes = m.to_bytes((m.bit_length()+ 7)// 8 ,byteorder='big' )
    message = message_bytes.decode("utf-8")
    return message
     


message = "Hello World! This is Sherlock."


def create_signature(message): 

    hashed = SHA256.new(message.encode('utf-8')).digest()
    hashed_int = int.from_bytes(hashed, byteorder='big')
    s = square_multiply (hashed_int, rsakey.d, rsakey.n)
    return s, hashed

def verify_signature(message):
    signature, hash = create_signature(message)
    x = square_multiply(signature, rsakey.e, rsakey.n)
    x_bytes = x.to_bytes((x.bit_length()+ 7)// 8 ,byteorder='big' )
    print("Final hash is the same :", hash == x_bytes )
    return 



verify_signature(message)