import re


text = input("Napishi: ")

pattern = r'ab{2,3}'


if re.fullmatch(pattern, text):
    print("Match")
else:
    print("No match")
