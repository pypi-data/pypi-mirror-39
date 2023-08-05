class cleanATOM(object):
    def __init__(self, filename):
        self.__filename=filename
    def clean(self):
        f=open(self.__filename, "r")
        newname=self.__filename[:-3]
        newname+='cleanATOM.pdb'
        f2=open(newname, "w")
        for i in f:
            i=i.strip()
            if (i[0]=="A" and i[1]=="T" and i[2]=="O" and i[3]=="M") or (i[0]=="H" and i[1]=="E" and i[2]=="T" and i[3]=="A"):
                f2.write(i)
                f2.write('\n')
        f.close()
        f2.close()
        
        
class insertTER(object):
    def __init__(self, filename):
        self.__filename=filename
    def insert(self):
        f3=open(self.__filename, "r")
        newname=self.__filename[:4]
        newname+='.insertTER.pdb'
        f4=open(newname, "w")
        prev_chain=''
        curr_chain=''
        for i in f3:
        
            i=i.rstrip()
            curr_chain=i[21]
            if (prev_chain.isalpha() and curr_chain.isalpha()) and (prev_chain!=curr_chain):
                f4.write(i)
                f4.write('\n')
                f4.write("TER")
                f4.write("    ")
                f4.write(i[7]+i[8]+i[9]+i[10]+i[11]+i[12]+i[13]+
                     i[14]+i[15]+i[16]+i[17]+i[18]+i[19]+i[20]
                     +i[21]+i[22]+i[23]+i[24]+i[25])
                f4.write('\n')
            else:
                f4.write(i)
                f4.write('\n')
            prev_chain=curr_chain
        f3.close()
        f4.close()

class alignATOM(object):
    def __init__(self, filename):
        self.__filename=filename
    def align(self):
        f5=open(self.__filename, "r")
        newname=self.__filename[:4]
        newname+='.alignATOM.pdb'
        f6=open(newname, "w")
        for i in f5:
            i=i.rstrip()
            if i[12]!=' ' and len(i)==77:
                #print (i)
                #print (i[12], len(i))
                #print (i[:12]+' '+i[12:])
                temp=i[:12]+' '+i[12:]
                f6.write(temp)
                f6.write('\n')
            else:
                f6.write(i)
                f6.write('\n')
        f5.close()
        f6.close()

class removeDUPLICATE(object):
    def __init__(self, filename):
        self.__filename=filename
    def remove(self):
        f7=open(self.__filename, "r")
        newname=self.__filename[:4]
        newname+='.removeDUPLICATE.pdb'
        f8=open(newname, "w")
        for i in f7:
            i=i.rstrip()
            if i[10]=='5' and i[9]==' ':
                temp=''
                for ii in range(len(i)):
                    if ii==14:
                        temp+='B'
                    else:
                        temp+=i[ii]
                f8.write(temp)
                f8.write('\n')
            else:
                f8.write(i)
                f8.write('\n')
        f7.close()
        f8.close()

class numberRESIDUE(object):
    def __init__(self, filename):
        self.__filename=filename
    def number(self):
        f9=open(self.__filename, "r")
        newname=self.__filename[:4]
        newname+='.numberRESIDUE.pdb'
        f10=open(newname, "w")
        for i in f9:
            i=i.rstrip()
            if i[17]=='I' and i[18]=='L' and i[19]=='E' and i[24]=='3' and i[25]=='2':
                temp=''
                for l in range(len(i)):
                    if l==25 and i[l]=='2':
                        temp+='1'
                    else:
                        temp+=i[l]
                f10.write(temp)
                f10.write('\n')
            else:
                f10.write(i)
                f10.write('\n')   
        f9.close()
        f10.close()
