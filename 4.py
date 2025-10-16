import re

text = input("Napishi: ")

pattern = r'[A-Z][a-z]+'


matches = re.findall(pattern, text)

if matches:
    print("Matches found:", matches)
else:
    print("No match")
