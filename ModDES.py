import sys
p=sys.version_info[0]

class _baseDES(object):
    def __init__(self,IV=None):
        if IV:
            IV=self.verifyNoUnicode(IV)
        self.blockSize=8
        if IV and len(IV)!=self.blockSize:
            raise ValueError("Invalid Initial Value IV, must be a multiple of "+str(self.blockSize)+" bytes")
        self.iv=IV

    def getKey(self):
        return self.__key
    def setKey(self, k):
        k=self.verifyNoUnicode(k)
        self.__key=k
    def getIV(self):
        return self.iv
    def setIV(self, IV):
        if not IV or len(IV)!= blockSize:
            raise ValueError("Invalid Initial Value IV, must be a multiple of "+str(self.blockSize)+" bytes")
        IV=self.verifyNoUnicode(IV)
        self._iv=IV
    def _padData(self,data):
        l=8-(len(data)%self.blockSize)
        if p<3:
            data+=l*chr(l)
        else:
            data+=bytes([l]*l)
        return data
    def _unpadData(self,data):
        if p<3:
            l=ord(data[-1])
        else:
            l=data[-1]
        data= data[:-l]
        return data
    def verifyNoUnicode(self, data):
        if p<3:
            if isinstance(data, unicode):
                raise ValueError("Program works only with byte strings, please don't enter Unicode Stings")
        else:
            if isinstance(data, str):
                try:
                    data.encode('ascii')
                except UnicodeEncodeError:
                    pass
                raise ValueError("Program works only with byte strings, please don't enter Unicode Stings")
        return data

class des(_baseDES):# The different matrices or databases were copied from internet to avoid any error.
    __pc1 = [56, 48, 40, 32, 24, 16,  8,
                  0, 57, 49, 41, 33, 25, 17,
                  9,  1, 58, 50, 42, 34, 26,
                 18, 10,  2, 59, 51, 43, 35,
                 62, 54, 46, 38, 30, 22, 14,
                  6, 61, 53, 45, 37, 29, 21,
                 13,  5, 60, 52, 44, 36, 28,
                 20, 12,  4, 27, 19, 11,  3
        ]

    __left_rotations = [
                1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1
        ]

    __pc2 = [
                13, 16, 10, 23,  0,  4,
                 2, 27, 14,  5, 20,  9,
                22, 18, 11,  3, 25,  7,
                15,  6, 26, 19, 12,  1,
                40, 51, 30, 36, 46, 54,
                29, 39, 50, 44, 32, 47,
                43, 48, 38, 55, 33, 52,
                45, 41, 49, 35, 28, 31
        ]

    __ip = [57, 49, 41, 33, 25, 17, 9,  1,
                59, 51, 43, 35, 27, 19, 11, 3,
                61, 53, 45, 37, 29, 21, 13, 5,
                63, 55, 47, 39, 31, 23, 15, 7,
                56, 48, 40, 32, 24, 16, 8,  0,
                58, 50, 42, 34, 26, 18, 10, 2,
                60, 52, 44, 36, 28, 20, 12, 4,
                62, 54, 46, 38, 30, 22, 14, 6
        ]

    __expansion_table = [
                31,  0,  1,  2,  3,  4,
                 3,  4,  5,  6,  7,  8,
                 7,  8,  9, 10, 11, 12,
                11, 12, 13, 14, 15, 16,
                15, 16, 17, 18, 19, 20,
                19, 20, 21, 22, 23, 24,
                23, 24, 25, 26, 27, 28,
                27, 28, 29, 30, 31,  0
        ]

    __sbox = [
                # S1
                [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
                 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
                 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
                 15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

                # S2
                [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
                 3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
                 0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
                 13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

                # S3
                [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
                 13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
                 13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
                 1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

                # S4
                [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
                 13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
                 10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
                 3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

                # S5
                [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
                 14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
                 4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
                 11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

                # S6
                [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
                 10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
                 9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
                 4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

                # S7
                [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
                 13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
                 1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
                 6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

                # S8
                [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
                 1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
                 7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
                 2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
        ]
    
    __p = [
                15, 6, 19, 20, 28, 11,
                27, 16, 0, 14, 22, 25,
                4, 17, 30, 9, 1, 7,
                23,13, 31, 26, 2, 8,
                18, 12, 29, 5, 21, 10,
                3, 24
        ]

    __fp = [
                39,  7, 47, 15, 55, 23, 63, 31,
                38,  6, 46, 14, 54, 22, 62, 30,
                37,  5, 45, 13, 53, 21, 61, 29,
                36,  4, 44, 12, 52, 20, 60, 28,
                35,  3, 43, 11, 51, 19, 59, 27,
                34,  2, 42, 10, 50, 18, 58, 26,
                33,  1, 41,  9, 49, 17, 57, 25,
                32,  0, 40,  8, 48, 16, 56, 24
        ]
    
    Encrypt=0
    Decrypt=1

    def __init__(self, key, IV=None):
        if len(key)!=8:
            raise ValueError("Invalid DES Key size, Key must be 8 bytes long.")
        _baseDES.__init__(self,IV)
        self.key_size=8
        self.L=[]
        self.R=[]
        self.Kn=[[0]*48]*16
        self.final=[]
        self.setKey(key)

    def setKey(self, key):
        _baseDES.setKey(self, key)
        self.createsubkeys()

    def stringToBitlist(self, data):
        if p<3:
            data=[ord(c)for c in data]
        l=len(data)*8
        r=[0]*l
        pos=0
        for c in data:
            j=7
            while j>=0:
                if c & (1<<j) != 0:
                    r[pos]=1
                else:
                    r[pos]=0
                pos+=1
                j-=1
        return r
    def bitlistToString(self, data):
        r=[]
        pos=0
        c=0
        while pos<len(data):
            c+=data[pos]<<(7-(pos%8))
            if (pos%8)==7:
                r.append(c)
                c = 0
            pos += 1

        if p<3:
            return ''.join([ chr(c) for c in r])
        else:
            return bytes(r)
    def __permutate(self, table, block):
        return list(map(lambda x:block[x],table))

    def createsubkeys(self):
        key= self.__permutate(des.__pc1, self.stringToBitlist(self.getKey()))
        i=0
        self.L=key[:28]
        self.R=key[28:]
        while i<16:
            j=0
            while j<des.__left_rotations[i]:
                self.L.append(self.L[0])
                del self.L[0]
                self.R.append(self.R[0])
                del self.R[0]
                j += 1
            self.Kn[i] = self.__permutate(des.__pc2, self.L + self.R)
            i += 1
    def __des_crypt(self, block, cryptType):
        block=self.__permutate(des.__ip, block)
        self.L=block[:32]
        self.R=block[32:]
        if cryptType==des.Encrypt:
            i=0
            ich=1
        else:
            i=15
            ich=-1
        j=0
        while j<16:
            tempR=self.R[:]
            self.R=self.__permutate(des.__expansion_table, self.R)
            self.R=list(map(lambda x,y: x^y, self.R, self.Kn[i]))
            B=[self.R[:6], self.R[6:12], self.R[12:18], self.R[18:24], self.R[24:30], self.R[30:36], self.R[36:42], self.R[42:]]
            u=0
            Bn=[0]*32
            pos = 0
            while u<8:
                m=(B[u][0]<<1)+B[u][5]
                n=(B[u][1]<<3)+(B[u][2]<<2)+(B[u][3]<<1)+B[u][4]
                v=des.__sbox[u][(m << 4) + n]
                Bn[pos]=(v&8)>>3
                Bn[pos+1]=(v&4)>>2
                Bn[pos+2]=(v&2)>>1
                Bn[pos+3]=v&1
                pos+=4
                u+=1
        

            self.R=self.__permutate(des.__p,Bn)
            self.R=list(map(lambda x,y:x^y,self.R,self.L))
            self.L=tempR
            j+=1
            i+=ich
        self.final=self.__permutate(des.__fp,self.R+self.L)
        return self.final

    def crypt(self,data,cryptType):#CBC
        if not data:
            return ""
        if len(data)%self.blockSize!=0:
            if cryptType==des.Decrypt:
                raise ValueError("Invalid data length, datat must be a multiple of "+str(self.blockSize)+" bytes.\n")
            if not self.getPadding():
                raise ValueError("Invalid data length, data must be a multiple of " + str(self.block_size) + " bytes\n. Try setting the optional padding character")
            else:
                data += (self.block_size - (len(data) % self.block_size)) * self.getPadding()
        if self.getIV():
            iv=self.stringToBitlist(self.getIV())
        else:
            raise ValueError("For CBC mode, you require Initial Value for ciphering")

        i=0
        dict={}
        r=[]
        while i<len(data):
            block=self.stringToBitlist(data[i:i+8])
            if cryptType==des.Encrypt:
                block=list(map(lambda x,y:x^y,block,iv))
            processed_block=self.__des_crypt(block,cryptType)
            if cryptType==des.Decrypt:
                processed_block=list(map(lambda x,y:x^y, processed_block,iv))
                iv=block
            else:
                iv=processed_block
        
            r.append(self.bitlistToString(processed_block))
            i+=8
        if p<3:
            return "".join(r)
        else:
            return bytes.fromhex("").join(r)

    def encrypt(self,data):
        data=self.verifyNoUnicode(data)
        data=self._padData(data)
        return self.crypt(data,des.Encrypt)
    def decrypt(self, data):
        data=self.verifyNoUnicode(data)
        data=self.crypt(data,des.Decrypt)
        return self._unpadData(data)
                                    

def example_des():
        from time import time
        key=input("Enter 8 bytes string as Key:")
        iv=input("Enter 8 bytes string as Initial Value:")
        d=input("Enter txt file name as a string:")
        with open(d,'r') as File:
            data=File.read()

        print "Example of DES encryption using CBC mode\n\n"
        t = time()
        k = des(key,iv)
        print "Key      : " + k.getKey()
        print "\n\n"
        print "Data     : " + data
        print "\n\n"

        d = k.encrypt(data)
        print "Encrypted: " + d
        print "\n\n"

        d = k.decrypt(d)
        print "Decrypted: " + d
        print "\n\n"
        print "DES time taken: %f" % (time() - t)+" seconds."
        print "\n\n"
            
example_des()



















        
    
