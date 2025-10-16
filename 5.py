import re

text = input("Napishi: ")

pattern = r'^a.*b$'

if re.fullmatch(pattern, text):
    print("Match")
else:
    print("No match")
