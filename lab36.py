from datetime import date, timedelta

current_date = date.today()


new_date = current_date - timedelta(days=5)

print("Current date:", current_date)
print("Date five days ago:", new_date)
