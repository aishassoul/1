import re

text = input("Enter a camelCase string: ")


snake_text = re.sub(r'([A-Z])', r'_\1', text).lower()

if snake_text.startswith('_'):
    snake_text = snake_text[1:]

print("Snake case string:", snake_text)
