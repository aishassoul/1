import re


text = input("Napishi: ")


result = re.findall(r'[A-Z][a-z]*', text)


print("itog", result)
