from flask import jsonify
import sqlite3
import csv

def isUserIdValid(id):
    conn = sqlite3.connect('User Data/users.db')    # Path to database file
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE id = ?", (id,))
    exists = cursor.fetchone()
    if exists:
        print("id exists in database")
    else:
        print("id does NOT exist in databaser")
    return True if exists else False

# Parse string of ids and return array
def parseCarArray(idString):
    if idString.startswith('[') and idString.endswith(']'):
        cleanedStr = idString.strip("[]")
        if cleanedStr:
            return list(map(int, cleanedStr.split(",")))
    return []

def getCarIDArray(user_id):
    try: 
        with open('User Data/saved_cars.csv', mode='r') as file:
            csvReader = csv.DictReader(file)

            for row in csvReader:
                print(f"Processing row: {row}")  # Debugging: print row data

                try:
                    user_id_from_csv = int(row['User_ID'])
                    print(f"Comparing {user_id_from_csv} to {user_id}")
                    if user_id_from_csv == user_id:
                        print("User ID matched.")
                        carIds = parseCarArray(row['Car_IDs'])
                        print(f"Found Car_IDs for user {user_id}: {carIds}")
                        return carIds
                except ValueError as e:
                    print(f"ValueError: Could not convert User_ID to int in row {row} - {e}")
                except KeyError as e:
                    print(f"KeyError: Missing column in row {row} - {e}")
            
            print(f"No match for user {user_id}")
            return []  # No match found
    except FileNotFoundError:
        print("CSV file not found")
        return []
    except Exception as e:
        print(f"Unexpected error in getCarIDArray: {e}")
        return [2]
    

def getSavedCars():

    id=3

    if isUserIdValid(id): 
        carArray = getCarIDArray(id)
        print("carArray:",carArray)

getSavedCars()