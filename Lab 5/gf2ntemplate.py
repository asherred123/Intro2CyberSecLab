# 50.042 FCS Lab 5 Modular Arithmetic
# Year 2024

from copy import deepcopy
# add is xor operation
# mul is and operation
class Polynomial2:
    def __init__(self,coeffs):
        self.coeffs = coeffs
        # coeffs is a list of coefficients
        # coeffs[0] is the coefficient of x^0
        pass
    def add(self,p2):
        #xor operation
        list1 = self.coeffs
        list2 = p2.coeffs
    
        #find the max length
        min_length = min(len(list1), len(list2))
        max_length = max(len(list1), len(list2))
        #perform xor operation
        result = []
        for i in range(max_length):
            if i < min_length:
                result.append(list1[i] ^ list2[i])
            else:
                if len(list1) > len(list2):
                    result.append(list1[i])
                else:
                    result.append(list2[i])
        return Polynomial2(result)

    def sub(self,p2):
        #xor operation
        list1 = self.coeffs
        list2 = p2.coeffs
    
        #find the max length
        min_length = min(len(list1), len(list2))
        max_length = max(len(list1), len(list2))
        #perform xor operation
        result = []
        for i in range(max_length):
            if i < min_length:
                result.append(list1[i] ^ list2[i])
            else:
                if len(list1) > len(list2):
                    result.append(list1[i])
                else:
                    result.append(list2[i])
        return Polynomial2(result)

    def mul(self,p2,modp=None):
        # initialise new result
        new_coeffs = [0] * ((len(self.coeffs)) + len(p2.coeffs) -1)

        # generate partial result
        for i in range(len(p2.coeffs)):
            if p2.coeffs[i] == 1:
                partial_res = self.coeffs[:]        # make a copy first
                partial_res += [0]*i                # shift left by i bits
                for j in range(len(partial_res)):
                    new_coeffs[j] = new_coeffs[j] ^ partial_res[j] # update new_coeffs

        # perform modulus reduction if necessary
        if modp != None:
            mod_len = len(modp.coeffs)
            while len(new_coeffs) >= mod_len:
                if new_coeffs[0] == 1:          # MSB = 1
                    for k in range(mod_len):    
                        new_coeffs[k] = new_coeffs[k] ^ modp.coeffs[k] # XOR with modp
                new_coeffs.pop(0) # remove first element

        return Polynomial2(new_coeffs)
    @property
    def deg(self):
        return len(self.coeffs) - 1

    @property
    def lc(self):
        return self.coeffs[-1]

    def div(self,p2):
        """
        using euclidean division
        deg = degree of argument
        lc = leading coefficient (highest degree of variable)
        """
        q,r = Polynomial2([0]), deepcopy(self)

        b,c = p2, p2.lc
        

        if (r.deg >= p2.deg):
            s = Polynomial2([0 for i in range(r.deg - p2.deg)] + [1])
            q = s.add(q)
            r = r.sub(s.mul(b))

        return q, r


    def __str__(self):
        list1 = self.coeffs
        string = ""
        
        # Iterate from the highest degree term to the lowest
        for i in range(len(list1) - 1, -1, -1):
            if list1[i] != 0:
                if i == 0:
                    string += "1" if list1[i] == 1 else str(list1[i])
                elif i == 1:
                    string += "x" if list1[i] == 1 else f"{list1[i]}x"
                else:
                    string += f"x^{i}" if list1[i] == 1 else f"{list1[i]}x^{i}"
                # Add the plus sign for all terms except the last one added
                if i != 0:
                    string += "+"

        # Remove the trailing ' + ' if it exists
        if string.endswith("+"):
            string = string[:-3]
        
        return string

 

    def getInt(p):
        result = 0
        for index,coeff in enumerate(p.coeffs):
            result += coeff * (2**index)
            
        return result



class GF2N:
    affinemat=[[1,0,0,0,1,1,1,1],
               [1,1,0,0,0,1,1,1],
               [1,1,1,0,0,0,1,1],
               [1,1,1,1,0,0,0,1],
               [1,1,1,1,1,0,0,0],
               [0,1,1,1,1,1,0,0],
               [0,0,1,1,1,1,1,0],
               [0,0,0,1,1,1,1,1]]

    def __init__(self,x,n=8,ip=Polynomial2([1,1,0,1,1,0,0,0,1])):
        self.x  = x
        self.n = n
        self.ip = ip
        


    def add(self,g2):
        p1 = self.getPolynomial2()
        p2 = g2.getPolynomial2()
        result = p1.mul(p2, self.ip)
     

        return GF2N(result.getInt(),self.n,self.ip)

    def sub(self, g2):
        return self.add(g2.p)

    def mul(self, g2):
        p1 = self.getPolynomial2()
        p2 = g2.getPolynomial2()
        result = p1.mul(p2, self.ip)
        return GF2N(result.getInt(), self.n, self.ip)

    def div(self, g2):
        p1 = self.getPolynomial2()
        p2 = g2.getPolynomial2()

        quotient, remainder = p1.div(p2)
        quotient, remainder = quotient.getInt(), remainder.getInt()
        return GF2N(quotient, self.n, self.ip), GF2N(remainder, self.n, self.ip)

    def getPolynomial2(self):
        """
        change int input to polynomial
        1. change self to binary, take note of 1
        2. if 1 --> coefficient = 1
        """
        binary = bin(self.x)[2:]
        polynomial = Polynomial2([int(x) for x in binary][::-1])

        return polynomial

    def __str__(self):
        return str(self.getPolynomial2().getInt())

    def getInt(self):
        return self.getPolynomial2().getInt()

    def mulInv(self):
        pass

    def affineMap(self):
        pass

print('\nTest 1')
print('======')
print('p1=x^5+x^2+x')
print('p2=x^3+x^2+1')
p1=Polynomial2([0,1,1,0,0,1])
print('p1=',p1)
p2=Polynomial2([1,0,1,1])
p3=p1.add(p2)
print('p3= p1+p2 = ',p3)

print('\nTest 2')
print('======')
print('p4=x^7+x^4+x^3+x^2+x')
print('modp=x^8+x^7+x^5+x^4+1')
p4=Polynomial2([0,1,1,1,1,0,0,1])
modp=Polynomial2([1,0,0,0,1,1,0,1,1])
p5=p1.mul(p4,modp)
print('p5=p1*p4 mod (modp)=',p5)

print('\nTest 3')
print('======')
print('p6=x^12+x^7+x^2')
print('p7=x^8+x^4+x^3+x+1')
p6=Polynomial2([0,0,1,0,0,0,0,1,0,0,0,0,1])    
p7=Polynomial2([1,1,0,1,1,0,0,0,1])
p8q,p8r=p6.div(p7)
print('q for p6/p7=',p8q)
print('r for p6/p7=',p8r)

print('\nTest 4')
print('======')
g1=GF2N(100)
g2=GF2N(5)
print('g1 = ',g1.getPolynomial2())
print('g2 = ',g2.getPolynomial2())
g3=g1.add(g2)
print('g1+g2 = ',g3)

print('\nTest 5')
print('======')
ip=Polynomial2([1,1,0,0,1])
print('irreducible polynomial',ip)
g4=GF2N(0b1101,4,ip)
g5=GF2N(0b110,4,ip)
print('g4 = ',g4.getPolynomial2())
print('g5 = ',g5.getPolynomial2())
g6=g4.mul(g5)
print('g4 x g5 = ',g6.ip)

print('\nTest 6')
print('======')
g7=GF2N(0b1000010000100,13,None)
g8=GF2N(0b100011011,13,None)
print('g7 = ',g7.getPolynomial2())
print('g8 = ',g8.getPolynomial2())
q,r=g7.div(g8)
print('g7/g8 =')
print('q = ',q.getPolynomial2())
print('r = ',r.getPolynomial2())

print('\nTest 7')
print('======')
ip=Polynomial2([1,1,0,0,1])
print('irreducible polynomial',ip)
g9=GF2N(0b101,4,ip)
print('g9 = ',g9.getPolynomial2())
print('inverse of g9 =',g9.mulInv().getPolynomial2())

print('\nTest 8')
print('======')
ip=Polynomial2([1,1,0,1,1,0,0,0,1])
print('irreducible polynomial',ip)
g10=GF2N(0xc2,8,ip)
print('g10 = 0xc2')
g11=g10.mulInv()
print('inverse of g10 = g11 =', hex(g11.getInt()))
g12=g11.affineMap()
print('affine map of g11 =',hex(g12.getInt()))