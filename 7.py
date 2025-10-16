import re

text = input("Enter a snake_case string: ")

def snake_to_camel(snake_str):
    parts = snake_str.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

camel_text = snake_to_camel(text)

print("Camel case string:", camel_text)
