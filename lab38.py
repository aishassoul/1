from datetime import datetime

current_datetime = datetime.now()

new_datetime = current_datetime.replace(microsecond=0)

print("Before removing microseconds:", current_datetime)
print("After removing microseconds:", new_datetime)
