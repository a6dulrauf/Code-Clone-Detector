from com.vsa.elements.Operators import Operators as op
from com.vsa.elements.Operands import Operands as oprn

import sys
from math import log2
class HalsteadMetrics:
  
    def __init__(self):    
        self.var={}
        self._operators=dict()
        self.file_path=None
    
    def calculate_metrics(self):
       # print(op.plus)
       
        for line in self.readFile():
            #for ch in line.split(' '): 

            if line.strip():
                #print(line)
                self.calculate_operators(line)
                self.calculate_operands(line)
                
    def calculate_operators(self,line):
        self.calculate_airthmetic_opr(line)
        self.calculate_logical_opr(line)
        
    def calculate_operands(self,line):
        for opr in oprn.operands_list:
            if line.__contains__(opr):
                self.update_dict(opr)
        
    
    def calculate_logical_opr(self,line):
        for opr in op.logical_op:
            if line.__contains__(opr):
                self.update_dict(opr)
                
    def calculate_airthmetic_opr(self,line):
        j=-1
        for i in range(len(line)-1):
            
            is_unary_opr=False
            for opr in op.arthmetic_op:
                if line[i:i+2] in op.arthmetic_op and opr == line[i:i+2] :
                    j=i
                    is_unary_opr=True
                    print(len(line))
                    self.update_dict(opr)
                    break
                elif line[i] in op.arthmetic_op and line[i] == opr and not is_unary_opr:
                    self.update_dict(opr)
             
                    
                    
    
    def update_dict(self,key):
        if str(key) not in self._operators:
            self._operators[str(key)]=1
        else:
            self._operators[str(key)]+=1
    
    def readFile(self):
        if self.file_path is not '':
            try:    
                with open(self.file_path,'r') as file:
                    return file.readlines()
                    #lines=[line for line in file.readlines()]
                #return lines
            except Exception as e:
                print(e.__str__())
                
    # all getters
                
    def get_all_operators(self):
        return [(key,val) for key,val in self._operators.items()]
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    #---------------------------------------------------------------------
    def run(self,programFileName):
        '''
        if(len(sys.argv) != 2):
            print("Usage: python3 halstead.py name_of_program")
        '''
        operatorsFileName = 'C:\\Users\ACE\\PycharmProjects\\CodeCloneDetector\\com\\vsa\\elements\\operators'
        programFileName = programFileName
        
        operators = {}
        operands = {}
        
        with open(operatorsFileName) as f:
            for ops in f:
                operators[ops.replace('\n','')] = 0
        
        isAllowed = True
        
        with open(programFileName) as f:
            for line in f:
                line = line.strip("\n").strip(' ')
        
                if(line.startswith("/*")):
                    isAllowed = False
               
                if((not line.startswith("//")) and isAllowed == True and (not line.startswith('#'))):
                    for key in operators.keys():
                        operators[key] = operators[key] + line.count(key)
                        line = line.replace(key,' ')
                    for key in line.split():
                        if key in operands:
                            operands[key] = operands[key] + 1
                        else:
                            operands[key] = 1
        
                if(line.endswith("*/")):
                    isAllowed = True
        
        '''
        n1, N1, n2, N2 = 0, 0, 0, 0
        
        print("OPERATORS:\n")
        for key in operators:
            if(operators[key] > 0):
                if(key not in ")}]"):
                    n1, N1 = n1 + 1, N1 + operators[key]
                    print("{} = {}".format(key, operators[key]))
        
        print("\nOPERANDS\n")
        for key in operands.keys():
            if(operands[key] > 0):
                n2, N2 = n2 + 1, N2 + operands[key]
                print("{} = {}".format(key, operands[key]))
        
        val = {"N": N1 + N2, "n": n1 + n2, "V": (N1 + N2) * log2(n1 + n2), "D": n1 * N2 / 2 / n2}
        val['E'] = val['D'] * val['V']
        val['L'] = val['V'] / val['D'] / val['D']
        val['I'] = val['V'] / val['D']
        val['T'] = val['E'] / (18)
        val['N^'] = n1 * log2(n1) + n2 * log2(n2)
        val['L^'] = 2 * n2 / N2 / n1
        
        unit = {'V': 'bits', 'T': 'seconds'}
        name = {'N':'Halstead Program Length', 'n':'Halstead Vocabulary', 'V':'Program Volume', 'D':'Program Difficulty', 'E': 'Programming Effort', 'L':'Language level', 'I':'Intelligence Content', 'T':'Programming time','N^':'Estimated program length', 'L^':'Estimated language level'}
        
        print("\nThe various values are: ")
        for key in val.keys():
            print("{} ({}) = {} {}".format(key,name[key], val[key], unit[key] if key in unit else ''))
        '''
        return [operators,operands] 
    
    
    
    