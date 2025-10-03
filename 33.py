import math

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def show(self):
        
        print(f"({self.x}, {self.y})")

    def move(self, x, y):
       
        self.x = x
        self.y = y

    def dist(self, other):
       
        return math.hypot(self.x - other.x, self.y - other.y)



p1 = Point(0, 0)
p2 = Point(3, 4)

p1.show()  
p2.show()   

print("Расстояние между p1 и p2:", p1.dist(p2))  

p1.move(2, -1)
p1.show()   
