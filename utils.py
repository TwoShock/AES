import pickle

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


