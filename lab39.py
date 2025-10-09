from datetime import datetime


date1 = datetime(2025, 10, 9, 12, 0, 0)
date2 = datetime(2025, 10, 8, 11, 30, 0)


difference = date1 - date2

seconds = difference.total_seconds()

print("Date 1:", date1)
print("Date 2:", date2)
print("Difference in seconds:", seconds)
