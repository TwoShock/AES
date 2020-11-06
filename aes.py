from utils import readObject,hexXOR,binaryXOR,convertHexToBinary,multiply,convertBinaryToHex
import numpy as np

class AES():
    def __init__(self,key,msg):
        self.__key = self.__transformInputToMatrix(key)
        self.__state = self.__transformInputToMatrix(msg)
        self.__sBox = readObject('./tables/sbox.pkl')
        self.__invSBox = readObject('./tables/inv_sbox.pkl')
        self.__mCols = readObject('./tables/mcols.pkl')
        self.__invMCols = readObject('./tables/inv_mcols.pkl')
        self.__rcon = ['01','02','04','08','10','20','40','80','1b','36']
        self.__rconVectors = [[r,'00','00','00'] for r in self.__rcon ]
        self.__keys = self.__keyExpansion()
        self.__output = ''
    def __transformInputToMatrix(self,input:str)->np.array:
        '''
        Transforms input to n by n matrix.
        '''
        inputMatrix = [input[i:i+2] for i in range (0,len(input),2)]
        inputMatrix = np.array(inputMatrix).reshape(4,4,order='F')
        return inputMatrix

    def __addRoundKey(self,key):
        '''
        Performs add round key operation on current state with current key.
        '''
        self.__state = np.array([[hexXOR(key[row][col],self.__state[row][col]) for col in range(len(self.__state))] for row in range(len(self.__state))])
        pad = np.vectorize(lambda x : '0' + x if len(x) == 1 else x)
        self.__state = pad(self.__state)
    
    def __byteSubstitution(self,inv = False):
        '''
        Performs byte substitution on current state.
        '''
        sBox = self.__sBox if inv == False  else self.__invSBox
        sub = np.vectorize(lambda x : sBox[int(x[0],16)][int(x[1],16)])
        self.__state = sub(self.__state)

    def __shiftRows(self,inv = False):
       '''
       Performs shift rows on current state.
       '''
       for i in range(4):
           if(inv):
               self.__state[i] = np.roll(self.__state[i],i)
           else:
               self.__state[i] = np.roll(self.__state[i],-i)
               

    def __mixColumns(self,inv = False):
        '''
        Performs mix column on current state.
        '''
        newState = [['00000000' for j in range(len(self.__state))]for i in range(len(self.__state))]
        mCols = self.__mCols if inv == False else self.__invMCols
        for i in range(len(self.__state)):
            for j in range(len(self.__state)):
                for k in range(len(self.__state)):
                    x = convertHexToBinary(mCols[i][k]).zfill(8)
                    y = convertHexToBinary(self.__state[k][j]).zfill(8)
                    product = multiply(x,y).zfill(8)
                    newState[i][j] = binaryXOR(newState[i][j],product)
        newState = np.array(newState)
        hexify = np.vectorize(lambda x:convertBinaryToHex(x)[2:])
        pad = np.vectorize(lambda x : '0' + x if len(x) == 1 else x)
        self.__state = pad(hexify(newState))

    def __xorVectors(self,v1,v2):
        '''
        Helper funciton for aes mix columns. It xors the results of the hex vectors and returns the hex vector result.
        '''
        out = []
        for i,v in enumerate(v1):
            b1 = convertHexToBinary(v).zfill(8)
            b2 = convertHexToBinary(v2[i]).zfill(8)
            res = convertBinaryToHex(binaryXOR(b1,b2))[2:]
            res = '0'+res if len(res) == 1 else res
            out.append(res)
        return np.array(out)

    def __keyExpansion(self):
        '''
        Handles key expansion for both encryption and decryption
        '''
        w = [self.__key[:,i] for i in range(len(self.__key))]
        sub = np.vectorize(lambda x : self.__sBox[int(x[0],16)][int(x[1],16)])
        j = 0
        for i in range(4,44):
            temp = w[i-1]
            if(i % 4 == 0):
               temp = sub(np.roll(temp,-1)) 
               temp = self.__xorVectors(temp,self.__rconVectors[j])
               j+=1
            w.append(self.__xorVectors(temp,w[i-4]))
        keys = [np.array(w[i:i+4]) for i in range(0,len(w),4)]
        keys = [np.transpose(keys[i]) for i in range(len(keys))]
        return keys
    def __appendMatrixToOutput(self,matrix):
        '''
        appends item to current output
        '''
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                self.__output += f'{matrix[i][j]} '
            self.__output +=f'\n'
    def getOutput(self):
       return self.__output 
    def encrypt(self):
        '''
        Performs the 10 round encryption of AES.
        '''
        state = self.__state
        key = self.__key
        self.__output += 'Performing AES Encryption...\n'
        self.__output += 'Current Key:\n'
        self.__appendMatrixToOutput(self.__key)
        self.__output +='\nAfter Intial add round key:\n'
        self.__appendMatrixToOutput(self.__state)
        self.__addRoundKey(self.__keys[0])
        for i in range(1,11):
            self.__output += '\nCurrent Key:\n'
            self.__appendMatrixToOutput(self.__keys[i])
            self.__byteSubstitution()
            self.__output += '\nAfter Byte substitution:\n'
            self.__appendMatrixToOutput(self.__state)
            self.__output += '\nAfter Shift Rows:\n'
            self.__shiftRows()
            self.__appendMatrixToOutput(self.__state)
            if(i != 10):
                self.__output += '\nAfter Mix Columns:\n'
                self.__mixColumns()
                self.__appendMatrixToOutput(self.__state)
            self.__output += '\nAfter Add Round Key:\n'
            self.__addRoundKey(self.__keys[i])
            self.__appendMatrixToOutput(self.__keys[i])
            self.__output += f'\nResult of Round {i}:\n'
            self.__appendMatrixToOutput(self.__state)
        self.__state = state
        self.__key == key

    def decrypt(self):
        '''
        Performs 10 round decryption of AES.
        '''
        state = self.__state
        key = self.__state

        keys = self.__keys[::-1]
        self.__addRoundKey(keys[0])
        self.__output += 'Performing AES Decryption...\n'
        self.__output += 'Current Key:\n'
        self.__appendMatrixToOutput(self.__key)
        self.__output +='\nAfter Intial add round key:\n'
        self.__appendMatrixToOutput(self.__state)
        for i in range(1,11):
            self.__output += '\nCurrent Key:\n'
            self.__appendMatrixToOutput(self.__keys[i])
            self.__byteSubstitution(inv=True)
            self.__output += '\nAfter Inverse Byte substitution:\n'
            self.__appendMatrixToOutput(self.__state)
            self.__output += '\nAfter Inverse Shift Rows:\n'
            self.__shiftRows(inv = True)
            self.__appendMatrixToOutput(self.__state)
            if(i != 10):
                self.__output += '\nAfter Inverse Mix Columns:\n'
                self.__mixColumns(inv=True)
                self.__appendMatrixToOutput(self.__state)
            self.__output += '\nAfter Add Round Key:\n'
            self.__addRoundKey(self.__keys[i])
            self.__appendMatrixToOutput(self.__keys[i])
            self.__output += f'\nResult of Round {i}:\n'
            self.__appendMatrixToOutput(self.__state)
        self.__state = state
        self.__key == key

