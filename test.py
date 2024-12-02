import csv

def parseCarArray(idString):
    if idString.startswith('[') and idString.endswith(']'):
        cleanedStr = idString.strip("[]").strip()
        if cleanedStr:
            return list(map(int, cleanedStr.split(",")))
    return []

id = "2"  # Match the ID as a string, since CSV fields are strings
carId = 9999

# Read the file
with open('User Data/saved_cars.csv', mode='r') as file:
    reader = csv.DictReader(file)
    rows = list(reader)

# Modify the rows
for row in rows:
    if row['User_ID'] == id:  # Ensure 'id' matches as a string
        car_ids = parseCarArray(row['Car_IDs'])
        car_ids.append(carId)  # Add the new car ID
        row['Car_IDs'] = str(car_ids)  # Update the Car_IDs field

# Write the updated data back to the file
with open('User Data/saved_cars.csv', mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)