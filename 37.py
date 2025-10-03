def fahrenheit_to_celsius(f):
    c = (5 / 9) * (f - 32)
    return c


f = float(input("Введите температуру в Фаренгейтах: "))
c = fahrenheit_to_celsius(f)
print("Температура в Цельсиях:", c)
