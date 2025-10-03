import math

def sphere_volume(r):
    volume = (4/3) * math.pi * (r**3)
    return volume


print(sphere_volume(1))  
print(sphere_volume(3))  
