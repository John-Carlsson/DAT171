# 7.2
# 
# Define a class named Shape and its subclass Square. 
# The Square class has an init function which takes a length as argument. 
# Both classes have a area function which can print the area of the shape where Shape's area is 0 by default.

class shape():
    def __init__(self):
        pass

    def area(self):
        return 0

class square(shape):
    def __init__(self,lengt):
        shape().__init__()
        self.length = lengt

    def get_length(self):
        return self.length
    
    def area(self):
        return self.get_length()

if __name__ =='__main__':
    figur = square(4)
    print(figur.area())