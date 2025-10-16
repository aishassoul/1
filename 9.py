import re

text = input("Napishi: ")

result = re.sub(r'(?<!^)(?=[A-Z])', ' ', text)


print("Text with spaces:", result)
