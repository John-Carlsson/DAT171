#Question:

#Write a program to solve a classic ancient Chinese puzzle:
#We count 35 heads and 94 legs among the chickens and rabbits in a farm. How many rabbits and how many chickens do we have?

#Hint:
#Use for loop to iterate all possible solutions.



if __name__ == '__main__':
    legs = 94
    heads = 35
    num_animals = 35
    max_num_rabbits = round(legs/4)-1

    for i in range(max_num_rabbits+1):
        r = i
        c = (legs-4*r)/2
        print('antalet kaniner:',r,'antalet höns:',c)