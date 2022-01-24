
import matplotlib.pyplot as plt

def tea(names,colors):
    for name in names:
        for col in colors:
            print('{nam} do you like {color} tea?'.format(nam=name,color= col))
    



if __name__ == '__main__':

    names = ['John', 'Lucas', 'Olle', 'Filip']
    colors = ['green', 'red', 'black']
    # tea(names,colors)




