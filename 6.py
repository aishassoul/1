import re


text = input("Napishi: ")

pattern = r'[ ,.]'

replaced_text = re.sub(pattern, ':', text)

print("after replace", replaced_text)
