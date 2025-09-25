#Duplicate values will be ignored:
thisset = {"apple", "banana", "cherry", "apple"}

print(thisset)


thisset = {"apple", "banana", "cherry"}
print(len(thisset))



thisset = {"apple", "banana", "cherry"}

print("banana" not in thisset)




thisset = {"apple", "banana", "cherry"}

thisset.add("orange")

print(thisset)




thisset = {"apple", "banana", "cherry"}
mylist = ["kiwi", "orange"]

thisset.update(mylist)

print(thisset)



thisset = {"apple", "banana", "cherry"}

thisset.remove("banana")

print(thisset)






set1 = {"a", "b", "c"}
set2 = {1, 2, 3}

set3 = set1.union(set2)
print(set3)




set1 = {"a", "b", "c"}
set2 = {1, 2, 3}

set3 = set1 | set2
print(set3)



set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}

set3 = set1 - set2
print(set3)




set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}

set3 = set1 ^ set2
print(set3)