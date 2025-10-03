class Shape:
    def __init__(self):
        pass   
    def area(self):
        return 0   
    
class Square(Shape):
    def __init__(self, length):
        self.length = length  

    def area(self):
        return self.length * self.length   

s = Shape()
print("Площадь Shape:", s.area())   

sq = Square(5)
print("Площадь квадрата:", sq.area())  