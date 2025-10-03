
class StringClass:
    def __init__(self):
        self.s = ""

    def gerString(self):
        self.s =input('Write smth')

    def printString(self):
        print(self.s.upper())

obj = StringClass()   
obj.getString()      
obj.printString()  