import csv
user_id=4
# Add user to csv file for saved cars
new_row = [user_id, []]
with open('User Data/saved_cars.csv', mode='a', newline='') as file:
    csvWriter = csv.writer(file)
    csvWriter.writerow(new_row)