import time
import itertools
import hashlib 
import string

file_path = "C:\\Users\\leewe\\Desktop\\Cybersecurity ex3\\salted6.txt"
#open text file and read the hashes
with open(file_path, "r") as file:
    hashes = file.read().splitlines()




charset = string.ascii_lowercase + string.digits

def md5_hash(text):
    return hashlib.md5(text.encode()).hexdigest()



def bruteforce(charset=charset, length= 6, hashes=hashes): 
#all characters have a length of 6
    
    for attempt in itertools.product(charset, repeat=length):
        #start2 = time.time()
        attempt = ''.join(attempt)
        hashed_attempt = md5_hash(attempt)
        if hashed_attempt in hashes:
            print(f"Hash {hashed_attempt} matched password: {attempt}")
            #end2 = time.time()
            #print("hash broken in: " + str(end2 - start2))
            hashes.remove(hashed_attempt)
            if not hashes:
                return
    print("No match found for remaining hashes")

start = time.time()

bruteforce()
end = time.time()
print("total time: " +str(end - start))