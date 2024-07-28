from Crypto.PublicKey import RSA 


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
   
    m  = square_multiply(message,  rsakey.e, rsakey.n)

    return m 

def decrypt(cipher_text): 
    m = square_multiply(cipher_text , rsakey.d , rsakey.n)
  
    return m
     


def protocol_attack():
    message = 100 
    print("Encrypting: ", message)
    cipher_text = encrypt(message)
    print("Result: \n ", cipher_text)
    multiplier = square_multiply(2 , rsakey.e, rsakey.n)
    modified = cipher_text * (multiplier % rsakey.n)
    print("Modified to: \n", modified)
    print("Decrypted: ", decrypt(modified))


protocol_attack()
