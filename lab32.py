

#Write a program using generator to print the even numbers between 0 and n in comma separated form where n is input from console.

def even(n):
    for i in range(n+1):
        if i%2==0:
            yield i

n = int(input("Napishi chislo"))
print(','.join(str(num) for num in even(n) ))