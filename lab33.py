def div_by_3_and_4_generator(n):
    for i in range(n + 1):          
        if i % 3 == 0 and i % 4 == 0:  
            yield i             


n = int(input("Enter a number: "))


print(",".join(str(num) for num in div_by_3_and_4_generator(n)))


#Define a function with a generator which can iterate the numbers, which are divisible by 3 and 4, between a given range 0 and n.


