# Level 3
# 
# Question 21
# A robot moves in a plane starting from the original point (0,0). The robot can move toward UP, DOWN, LEFT and RIGHT with a given steps. The trace of robot movement is shown as the following:
# UP 5
# DOWN 3
# LEFT 3
# RIGHT 2
# ¡­
# The numbers after the direction are steps. Please write a program to compute the distance from current position after a sequence of movement and original point. If the distance is a float, then just print the nearest integer.
# Example:
# If the following tuples are given as input to the program:
# UP 5
# DOWN 3
# LEFT 3
# RIGHT 2
# Then, the output of the program should be:
# 2

import numpy
class robot():
    def __init__(self,x0=0,y0=0):
        self.start = {'x':x0,'y':y0}
        self.x = x0
        self.y = y0
    

    def right(self,num):
        self.x += num

    def up(self,num):
        self.y += num
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def distance_travelled(self):
        return numpy.sqrt(self.get_x()**2+self.get_y()**2)
        

input = [('UP', 5),('DOWN', 3),('LEFT', 3),('RIGHT', 2)]

if __name__ =='__main__':
    lollo = robot()
    for i in input:
        if i[0] == 'UP':
            lollo.up(i[1])
        elif i[0] == 'DOWN':
            lollo.up(-i[1])
        elif i[0] == 'LEFT':
            lollo.right(-i[1])
        elif i[0] == 'RIGHT':
            lollo.right(i[1])
    print(lollo.distance_travelled())












        
