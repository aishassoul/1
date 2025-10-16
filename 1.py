#Write a Python program that matches a string that has an 'a' followed by zero or more 'b''s

import re

text = input("Napishi: ")

pattern = r'ab*'

if re.fullmatch(pattern, text):
    print("Match")
else:
    print("No match")
