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


def alice_part():
 
    s = 142742489499464835091678061948619155018397573947887448498055944021478817743279328217299084248104892486741445836631310913787021333177615147874211038132373820518081302704045520113134530312085606334520232930277528690351763993356036098995593520354485603643863390206020364618208302808783801983158352937994536085221
    # Compute x ≡ s^e mod n
    x = square_multiply(s, rsakey.e, rsakey.n)
    
    
    return x, s

# Bob's Part
def bob_part( x, s):
 
    

    x_prime = square_multiply(s, rsakey.e, rsakey.n)
    
    # Check whether x' == x
    if x_prime == x:
        print("Signature is valid")
    else:
        print("Signature is invalid")

# Run the attack
x, s = alice_part()
bob_part( x, s)