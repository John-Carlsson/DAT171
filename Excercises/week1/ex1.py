""" Jag leker runt med klasser för att bli bekväm"""

import matplotlib

class Shape:
    def __init__(self,color=None):
        self.color = color

    def get_color(self):
        return self.color

class Square(Shape):
    def __init__(self,length=0,color='White'):
        super().__init__(color)
        self.side = length

    def get_side(self):
        return self.side

    def set_side(self,num):
        self.side = num

    def area(self):
        return self.side**2

s = Square(2,'Green')
print(s.color)