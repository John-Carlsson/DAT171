#Write a function to compute 5/0 and use try/except to catch the exceptions.

def fun():
    return 5/0

try:
    fun()
except ZeroDivisionError:
    print("division by zero!")

finally:
    print('In finally block for cleanup')

#Define a custom exception class which takes a string message as attribute.

class MyError(Exception):
    """My own exception class"""
    def __init__(self, msg):
        self.msg = msg


error = MyError('somethings wrong')



#Assuming that we have some email addresses in the "username@companyname.com" format,
#please write program to print the user name of a given email address. Both user names and company names are composed of letters only.
import re
def username(mail):
    if '@' in mail:
        pattern = "(\w+)@(\w+).(com)"
        split = re.match(pattern,mail)
        print('Ditt användarnamn är:', split[1], '\nditt företag heter:', split[2])


#Write a program which accepts a sequence of words separated by whitespace as input to print the words composed of digits only.

def onlynum(string):
    for a in string:
        if a.isdigit():
            print(a)


# Question:
# Define a function which can generate a dictionary where the keys are numbers between 1 and 20 (both included) and the
# values are square of keys. The function should just print the values only.
def square(num):
    l = list(range(1,num+1))
    d = {k:k**2 for k in l}
    print(d.values())

if __name__ == '__main__':
    #print('Skriv din mail')
    #mail = str(input())
    #m = username(mail)
    #
    mening = "2 katter springer ifatt 4 hundar"
   # onlynum(mening)

    square(20)