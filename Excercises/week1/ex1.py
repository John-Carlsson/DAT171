""" Jag leker runt med klasser för att bli bekväm"""

import sys
import numpy as np
import math
class Shape:
    def __init__(self,color=None):
        self.color = color

    def get_color(self):
        return self.color

class Triangle(Shape):
    def __init__(self,length,color='White'):
        super().__init__(color)
        self.sides = [length,length,length] # the different length of sides in a vector


    def get_sides(self):
        return self.sides

    def set_side(self,vec):
        self.sides = vec

    def get_area(self):
        s = 1/2*(sum(self.get_sides()))
        area = math.sqrt(s*(s-self.sides[0])*(s-self.sides[1])*(s-self.sides[1]))
        return area

class Square(Shape):
    def __init__(self,length=0,color='White'):
        super().__init__(color)
        self.side = float(length)


    def get_side(self):
        return self.side

    def set_side(self,num):
        self.side = num

    def get_area(self):
        return self.get_side()**2


def kvadrat():
    print('------- Ange längden på Kvadratens sida -------\n')
    l = input()
    print('------- vill du att kvadraten ska ha en färg? (y/n) -------\n')
    f = str(input())
    if f == 'y':
        print('--- Vilken Färg? ---')
        c = str(input())
    elif f == 'n':
        c = 'vit'
        pass
    return l,c

def triangel():
    print('------- Ange längerna på triangelns sida(x)(liksidig traiangel) -------\n')
    l = int(input())

    print('------- vill du att triangeln ska ha en färg? (y/n) -------\n')
    f = str(input()).lower()
    if f == 'y':
        print('--- Vilken Färg? ---')
        c = str(input())
    elif f == 'n':
        c = 'vit'
        pass
    return l,c

if __name__ == '__main__':


    print('------- vilken figur? (K/T) -------\n')
    r = input().lower()
    if r == 'k':
        l,c = kvadrat()
        s = Square(l,c)
    elif r == 't':
        l,c = triangel()    
        s = Triangle(l,c)
    print('\n')

    #s = Square(sys.argv[1],str(sys.argv[2]))
    
    print('Färgen på figuren är:',s.color)
    area = s.get_area()
    print('Figurens area är',area)