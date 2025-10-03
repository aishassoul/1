def unique_list(lst):
    unique = []
    for item in lst:
        if item not in unique:  
            unique.append(item)
    return unique



print(unique_list([1, 2, 2, 3, 4, 4, 5]))    
print(unique_list(["a", "b", "a", "c", "b"])) 
