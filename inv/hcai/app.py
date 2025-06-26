from datetime import date

# Get today's date
today = date.today()

# Format the date with the full month name
formatted_date = today.strftime("%B %d, %Y")

# Print the formatted date
print(formatted_date)