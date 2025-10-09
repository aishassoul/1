
#Create a generator that generates the squares of numbers up to some number N.

def square(n):
    for i in range (n, n+1):
        yield i**2

n=5
for s in square(n):
    print (s)