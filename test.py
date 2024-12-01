import csv
user_id = 4

# Data to be added
new_row_str = str(user_id)+',"[]"'

# Open the file in append mode with newline='' to control line breaks
with open('User Data/saved_cars.csv', mode='a', newline='') as file:
    file.write(new_row_str + '\n')