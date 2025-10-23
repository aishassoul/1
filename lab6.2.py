txt = input(str("napishi: "))

upp = sum(1 for i in txt if i.isupper())
low = sum(1 for i in txt if i.islower())

print("upper case :", upp)
print("lower case :", low)