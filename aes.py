from utils import readObject,hexXOR
import numpy as np

class AES():
    def __init__(self,key,msg):
        self.__key = self.__transformInputToMatrix(key)
        self.__state = self.__transformInputToMatrix(msg)
        self.__sBox = readObject('./tables/sbox.pkl')
        self.__invSBox = readObject('./tables/inv_sbox.pkl')
        self.__mCols = readObject('./tables/mcols.pkl')
        self.__invMCols = readObject('./tables/inv_mcols.pkl')
        self.__addRoundKey()
        self.__byteSubstitution()
        print(self.__state)

    def __transformInputToMatrix(self,input:str)->np.array:
        inputMatrix = [input[i:i+2] for i in range (0,len(input),2)]
        inputMatrix = np.array(inputMatrix).reshape(4,4,order='F')
        return inputMatrix

    def __addRoundKey(self):
        '''
        Performs add round key operation on current state with current key.
        '''
        self.__state = np.array([[hexXOR(self.__key[row][col],self.__state[row][col]) for col in range(len(self.__state))] for row in range(len(self.__state))])
        pad = np.vectorize(lambda x : '0' + x if len(x) == 1 else x)
        self.__state = pad(self.__state)
    
    def __byteSubstitution(self):
        '''
        Performs byte substitution on current state.
        '''
        sub = np.vectorize(lambda x : self.__sBox[int(x[0],16)][int(x[1],16)])
        self.__state = sub(self.__state)
    

key = '5468617473206D79204B756E67204675'
msg = '54776F204F6E65204E696E652054776F'
aes = AES(key,msg)

