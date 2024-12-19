from io import StringIO

test = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

class cpu:
    def __init__(self, program, rA=0, rB=0, rC=0):
        self.program = program
        self.rA = rA
        self.rB = rB
        self.rC = rC
        self.IP = 0
    
    def tick(self):
        
