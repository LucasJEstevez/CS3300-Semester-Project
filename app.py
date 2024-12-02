from flask import Flask, render_template, request, url_for, jsonify, make_response
from flask_jwt_extended import JWTManager, create_access_token, decode_token
from functools import wraps
from email_validator import validate_email, EmailNotValidError
from Code.Python.compare_csvs import compare_and_merge_csv
import requests
import os
import jinja2
import bcrypt
import sqlite3
import datetime
import jwt
import csv
import ast

#Initialize the Flask application 
app = Flask(__name__)


app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_KEY')
jwt = JWTManager(app)
print(f"JWT Secret Key: {os.environ.get('JWT_KEY')}")

# Function to construct the URL for the car price prediction API request 
def construct_url(car_info, key):

    # Base URL for the MarketCheck API with an API key and the car type set to 'used'
    url = f"https://mc-api.marketcheck.com/v2/predict/car/price?api_key={key}&car_type=used"
    
    vin = car_info.get('vin', None) #Retrieve the VIN if it is given by user, or None if not 

    if vin:
        # If VIN is provided include the VIN and mileage information in the URL
        url += f"&vin={car_info['vin']}&miles={car_info['miles1']}"
    else:
        # If no VIN is provided, use other car details 
        url += f"&miles={car_info['miles2']}&year={car_info['year']}&make={car_info['make']}&model={car_info['model']}&trim={car_info['trim']}"

    # Returns the constructed URL to be used for API requests
    return url

# Function to make the API request and retrieve car price prediction data 
def get_car_prediction(car_info, key, url):
    # Make a GET request to the contructed URL
    response = requests.get(url)

    # Check if the response status code indicates success
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
# Create route to index page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/price_prediction', methods=['POST'])
def price_prediction():
    # Get car data from submitted form
    car_info = {
        'vin': request.form.get('vin', None),
        'miles1': request.form.get('miles1', None),
        'year': request.form.get('year', None),
        'make': request.form.get('make', None),
        'model': request.form.get('model', None),
        'trim': request.form.get('trim', None),
        'miles2': request.form.get('miles2', None),
    }

    # Validate year is within the allowed range
    error="Error: Failed to retrieve prediction."
    vin = car_info.get('vin', None)
    if not vin:

        year = car_info.get('year')
        if not year or not year.isdigit():
            return render_template('index.html', error=error)
        
        year = int(year)
        if not (1975 <= year <= 2024):
            return render_template('index.html', error=error)

    # Retrieve API key from environment variable 
    key = os.environ.get('API_KEY')  # Ensure your API key is set as an environment variable

    # Construct the URL for the API request 
    url = construct_url(car_info, key)

    # Make the API request 
    prediction = get_car_prediction(car_info, key, url)

    # Check if prediction was succesful 
    if prediction:
        return render_template('index.html', prediction=prediction)
    else:
        return render_template('index.html', error=error)
   

#Create routes for each page
@app.route('/buy')
def buy_page():
    return render_template('Sidebar_Pages/buypage.html')

@app.route('/sell')
def sell_page():
    return render_template('Sidebar_Pages/sellpage.html')

@app.route('/contact')
def contact_page():
    return render_template('Sidebar_Pages/contactpage.html')

@app.route('/about')
def about_page():
    return render_template('Sidebar_Pages/aboutpage.html')

@app.route('/terms')
def terms_page():
    return render_template('Sidebar_Pages/terms.html')

@app.route('/register')
def register_page():
    return render_template('User_Pages/register.html')

@app.route('/sign-in')
def sign_in_page():
    return render_template('User_Pages/sign-in.html')

@app.route('/buytest')
def buy_test_page():
    return render_template('Sidebar_Pages/buypagetest.html')

@app.route('/saved-cars')
def saved_cars_page():
    return render_template('User_Pages/saved-cars.html')


# All code to do with login handling
USERNAME_NOT_IN_DATA = -1
INCORRECT_PASSWORD = -2

# Ensure login credentials are valid
def getUserId(tryUsername, tryPassword):
    # Opens database file
    conn = sqlite3.connect('User Data/users.db')  # Path to database file
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, password, email FROM users")
    rows = cursor.fetchall()
    conn.close()
    
    for row in rows:
        id, username, password, email = row

        # If the username the user entered matches either the username or email in the row
        if tryUsername == username or tryUsername == email:
            
            #Checks password against hash
            if bcrypt.checkpw(tryPassword.encode(), password.encode()):
                return id
            else:
                return INCORRECT_PASSWORD

    return USERNAME_NOT_IN_DATA

# Return username associated with user ID
def getUsername(userId):
    conn = sqlite3.connect('User Data/users.db')    # Path to database file
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE id = ?", (userId,))
    username = cursor.fetchone()
    conn.close()
    return username[0] if username else None

# Return username associated with user ID
def getEmail(userId):
    conn = sqlite3.connect('User Data/users.db')    # Path to database file
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users WHERE id = ?", (userId,))
    email = cursor.fetchone()
    conn.close()
    return email[0] if email else None

def isUserIdValid(id):
    conn = sqlite3.connect('User Data/users.db')    # Path to database file
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE id = ?", (id,))
    exists = cursor.fetchone()
    return True if exists else False

# Validate Email Address
def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except EmailNotValidError as e:
        return False

# Check if username already exists in database
def usernameTaken(newUser):
    # Opens database file
    conn = sqlite3.connect('User Data/users.db')  # Path to database file
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password, email FROM users")
    rows = cursor.fetchall()
    conn.close()
    
    for row in rows:
        id, username, password, email = row

        if newUser == username:
            return True
    
    return False

# Check if email already exists in database
def emailTaken(newEmail):

    # Open database file
    conn = sqlite3.connect('User Data/users.db')  # Path to database file
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password, email FROM users")
    rows = cursor.fetchall()
    conn.close()
    
    # For each user in database
    for row in rows:
        id, username, password, email = row

        if newEmail == email:
            return True
    
    return False

# Function to hash a password
def hash_password(password: str) -> str:
    # Generate a salt
    salt = bcrypt.gensalt()
    
    # Hash the password using the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    # Return the hashed password
    return hashed_password.decode('utf-8')

# Adds user to database
def addUserToDB(username,email,password):
    conn = sqlite3.connect('User Data/users.db')    # Path to database file

    cursor=conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL)''')
    
    cursor.execute('''INSERT INTO users (username, password, email) 
                        VALUES (?, ?, ?)''', (username, password, email))
    
    # Commit the change to users.db
    conn.commit()
    conn.close()

# Parse string of ids and return array
def parseCarArray(idString):
    if idString.startswith('[') and idString.endswith(']'):
        cleanedStr = idString.strip("[]").strip()
        if cleanedStr:
            return list(map(int, cleanedStr.split(",")))
    return []

# Gets ids of saved cars for user
def getCarIDArray(user_id):
    try: 
        with open('User Data/saved_cars.csv', mode='r') as file:
            csvReader = csv.DictReader(file)

            for row in csvReader:
                if int(row['User_ID']) == int(user_id):
                    carIds = parseCarArray(row['Car_IDs'])
                    return carIds
            return [-1]
    except FileNotFoundError:
        print("CSV file not found")
        return [-1]
    except Exception as e:
        print(f"Unexpected error in getCarIDArray: {e}")
        return [-1]
    
def getSaleIDArray(user_id):
    try: 
        with open('User Data/saved_cars.csv', mode='r') as file:
            csvReader = csv.DictReader(file)

            for row in csvReader:
                if int(row['User_ID']) == int(user_id):
                    carIds = parseCarArray(row['Sell_IDs'])
                    return carIds
            return [-1]
    except FileNotFoundError:
        print("CSV file not found")
        return [-1]
    except Exception as e:
        print(f"Unexpected error in getCarIDArray: {e}")
        return [-1]

# Handles POST request for login
@app.route('/login', methods=['POST'])
def login():

    # Get JSON data from the request
    data = request.get_json()

    # Validate the request data (should already be validated by client, but just in case)
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"message": "Error: Username or password is missing"}), 400

    # Extract username/email and password from data
    usernameOrEmail = data.get('username')
    password = data['password']

    # Get user ID from the database (will also get errors)
    user_id = getUserId(usernameOrEmail, password)

    # Invalid Logins
    if user_id == USERNAME_NOT_IN_DATA:
        return jsonify({"message": "Error: User does not exist"}), 401
    elif user_id == INCORRECT_PASSWORD:
        return jsonify({"message": "Error: Incorrect password"}), 401

    # Successful login, return token and success message
    token = create_access_token(
        identity=str(user_id),
        expires_delta=datetime.timedelta(hours=2)
    )
    return jsonify(access_token=token,message="Login successful!"), 200

@app.route('/register_account', methods=['POST'])
def register():
    # Get JSON data from the request
    data = request.get_json()

    # Validate the request data (should already be validated by client, but just in case)
    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({"message": "Error: Username or Email or Password is missing"}), 400
    
    # Extract info from request
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Errors
    if not is_valid_email(email):
       return jsonify({"message": "Error: Invalid email"}), 400

    if usernameTaken(username):
        return jsonify({"message":"Error: Username already taken"}), 409
    elif emailTaken(email):
        return jsonify({"message":"Error: Email already taken"}), 409

    # Add user to database
    hashed_password = hash_password(password)
    addUserToDB(username,email,hashed_password)
    user_id = getUserId(username,password)

    # Add user to csv file for saved cars
    new_row_str = str(user_id)+',"[]"'

    # Open the file in append mode with newline='' to control line breaks
    with open('User Data/saved_cars.csv', mode='a', newline='') as file:
        file.write(new_row_str + '\n')

    # Create token to send to browser
    token = create_access_token(
        identity=str(user_id),
        expires_delta=datetime.timedelta(hours=2)
    )
    
    # Send valid response to frontend
    return jsonify(access_token=token,message="Registration successful!"), 200

# Check if browser token is valid
@app.route('/isValidToken', methods=['POST'])
def isValidToken():

    # Get token from request
    data = request.get_json()
    token = data.get('token')
    if(token):

        # Decrypt token
        decoded = decode_token(token)
        id = decoded.get('sub')
        username = getUsername(id)
        if username:
            return jsonify({"isValid":True, "username": username})
        else:
            return jsonify({"isValid":False})
    else:
        return jsonify({"isValid":False})

@app.route('/getSavedCars', methods=['POST'])
def getSavedCars():

    # Get token from request
    data = request.get_json()
    token = data.get('token')
    if(token):

        # Decrypt token
        decoded = decode_token(token)
        id = decoded.get('sub')
        if isUserIdValid(id):
            carArray = getCarIDArray(id)
            if carArray != [-1]:
                return jsonify({"isValid":True, "error":False, "carIdArray": carArray})
            else:
                return jsonify({"isValid":True, "error":True})
        else:
            return jsonify({"isValid":False, "message":"userIdInvalid"})
    else:
        return jsonify({"isValid":False, "message":"no token"})

@app.route('getSaleCars', method=['POST'])
def getSaleCars():

    # Get token from request
    data = request.get_json()
    token = data.get('token')
    if(token):

        # Decrypt token
        decoded = decode_token(token)
        id = decoded.get('sub')
        if isUserIdValid(id):
            carArray = getSaleIDArray(id)
            if carArray != [-1]:
                return jsonify({"isValid":True, "error":False, "carIdArray": carArray})
            else:
                return jsonify({"isValid":True, "error":True})
        else:
            return jsonify({"isValid":False, "message":"userIdInvalid"})
    else:
        return jsonify({"isValid":False, "message":"no token"})
            

@app.route('/saveCar', methods=['POST'])
def saveCar():
    data = request.get_json()
    token = data.get('token')
    carId = data.get('id')
    if(token):

        decoded = decode_token(token)
        id = decoded.get('sub')

        if isUserIdValid(id):
            try: 
                # Read the file
                with open('User Data/saved_cars.csv', mode='r') as file:
                    reader = csv.DictReader(file)
                    rows = list(reader)

                # Modify the rows
                for row in rows:
                    if row['User_ID'] == id:  # Ensure 'id' matches as a string
                        car_ids = parseCarArray(row['Car_IDs'])
                        car_ids.append(int(carId))  # Add the new car ID
                        car_ids = list(sorted(set(car_ids)))
                        row['Car_IDs'] = str(car_ids)  # Update the Car_IDs field

                # Write the updated data back to the file
                with open('User Data/saved_cars.csv', mode='w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=rows[0].keys())
                    writer.writeheader()
                    writer.writerows(rows)
                
                return jsonify({"success":True})

            except FileNotFoundError:
                return jsonify({"success":False, "message": "file not found"})
            except Exception as e:
                return jsonify({"success":False, "message": e})

#Compares the available cars to sold cars in order to add a column to the buy page displaying it
#Uses startup_ran to only execute once, since flask discontinued start_before_request
startup_ran = False
@app.before_request
def run_startup_task():
    global startup_ran
    if not startup_ran:
        compare_and_merge_csv(
            file1=os.path.join(app.root_path, 'static/cars/site_available_cars.csv'),
            file2=os.path.join(app.root_path, 'static/cars/site_sold_cars.csv'),
            match_columns=[1, 2, 3],
            additional_column=6,
            output_file=os.path.join(app.root_path, 'static/cars/compared_available_cars.csv')
        )
        startup_ran = True


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use the PORT environment variable
    app.run(host='0.0.0.0', port=port)