from flask import Flask, render_template, request, url_for, jsonify, make_response
from flask_jwt_extended import JWTManager, create_access_token, decode_token
from functools import wraps
from email_validator import validate_email, EmailNotValidError
import requests
import os
import jinja2
import bcrypt
import sqlite3
import datetime
import jwt


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
        return render_template('index.html', error="Error: Failed to retrieve prediction.")
   

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

def getUserId(tryUsername, tryPassword):
    # Opens database file
    conn = sqlite3.connect('Data/userdata/users.db')  # Ensure this path is correct
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

def getUsername(userId):
    conn = sqlite3.connect('Data/userdata/users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE id = ?", (userId,))
    username = cursor.fetchone()
    conn.close()
    return username[0] if username else None

def getEmail(userId):
    conn = sqlite3.connect('Data/userdata/users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users WHERE id = ?", (userId,))
    email = cursor.fetchone()
    conn.close()
    return email[0] if email else None

# Function to validate email
def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except EmailNotValidError as e:
        return False

def usernameTaken(newUser):
    # Opens database file
    conn = sqlite3.connect('Data/userdata/users.db')  # Ensure this path is correct
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password, email FROM users")
    rows = cursor.fetchall()
    conn.close()
    
    for row in rows:
        id, username, password, email = row

        if newUser == username:
            return True
    
    return False

def emailTaken(newEmail):
    # Opens database file
    conn = sqlite3.connect('Data/userdata/users.db')  # Ensure this path is correct
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password, email FROM users")
    rows = cursor.fetchall()
    conn.close()
    
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
    conn = sqlite3.connect('Data/userdata/users.db')

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
    #token = create_access_token(identity={'userID': user_id}, expires_delta=datetime.timedelta(days=1))
    token = create_access_token(
        identity=str(user_id),
        expires_delta=datetime.timedelta(days=1)
    )
    # token = user_id
    return jsonify(access_token=token,message="Login successful!"), 200

@app.route('/register_account', methods=['POST'])
def register():
    # Get JSON data from the request
    data = request.get_json()

    #Validate the request data (should already be validated by client, but just in case)
    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({"message": "Error: Username or Email or Password is missing"}), 400
    
    # Extract info from request
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not is_valid_email(email):
       return jsonify({"message": "Error: Invalid email"}), 400

    if usernameTaken(username):
        return jsonify({"message":"Error: Username already taken"}), 409
    elif emailTaken(email):
        return jsonify({"message":"Error: Email already taken"}), 409

    hashed_password = hash_password(password)

    addUserToDB(username,email,hashed_password)
    user_id = getUserId(username,password)

    #token = create_access_token(identity={'userID': user_id}, expires_delta=datetime.timedelta(days=1))
    token = create_access_token(
        identity=str(user_id),
        expires_delta=datetime.timedelta(days=1)
    )
    # This is for testing
    jwt_key = os.environ.get('JWT_KEY')
    
    return jsonify(access_token=token,message="Registration successful!",key=jwt_key), 200


@app.route('/isValidToken', methods=['POST'])
def isValidToken():
    print("started isValidToken")
    data = request.get_json()
    print("data: ",data)
    token = data.get('token')
    if(token):
        print("Received token: ",token)
        decoded = decode_token(token)
        id = decoded.get('sub')
        username = getUsername(id)
        if(username):
            print("username valid")
            print("username: ",username)
            return jsonify({"isValid":True, "username": username})
        else:
            return jsonify({"isValid":False})
    else:
        return jsonify({"isValid":False})
    
# User data handling

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use the PORT environment variable
    app.run(host='0.0.0.0', port=port)