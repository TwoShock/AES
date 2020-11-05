import pickle
import functools
def readObject(filename:str)->str:
    '''
    Takes in filename and reads the pickled data stored in the file.
    Used for reading in the data for tables in aes.
    '''
    return pickle.load(open(filename,'rb'))
def binaryXOR(b1:str,b2:str):
    '''
    Computes the binary xor of two strings
    '''
    if(len(b1) >= len(b2)):
        b2 = b2.zfill(len(b1))
    else:
        b1 = b1.zfill(len(b2))
    return "".join(["0" if b1[i] == b2[i] else "1" for i in range(len(b1))])

def hexXOR(h1:str,h2:str)->str:
    '''
    computes the hex xor of two binary strings and returns results as hex
    '''
    return convertBinaryToHex(binaryXOR(convertHexToBinary(h1),convertHexToBinary(h2)))[2:]

def convertHexToBinary(hexStr):
    return bin(int(hexStr,16))[2:]
    
def convertBinaryToHex(binary):
    return str(hex(int(binary,2)))

def circularLeftShift(bits,n):
    bits = list(bits)
    return "".join(bits[n::] + bits[:n:])

def ciruclarRightShift(bits,n):
    bits = list(bits)
    return "".join(bits[n:len(bits):] + bits[0:n:])

def multiplyByX(p1):
    if p1[0] == '0':
        return circularLeftShift(p1,1)
    elif p1[0] == '1':
        p2 = p1
        p2 = '0' + p2[1:]
        p2 = circularLeftShift(p2,1)
        return binaryXOR(p2,'00011011')

def multiplyByXPowerN(p1,n):
    answer = p1
    for i in range(n):
        answer = multiplyByX(answer)
    return answer

def multiply(p1,p2):
    """
    multiplies two  polynomials in galois field 2^8
    """
    if(p2 == '00000000'):
        return '00000000'
    out = []
    i = len(p1)-1 
    for b in p2:
        if(b == '1'):
            out.append(multiplyByXPowerN(p1,i))
        i-=1
    answer = functools.reduce(lambda a,b:binaryXOR(a,b),out)
    return answer
