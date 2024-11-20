from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import bcrypt
import sqlite3

app = Flask(__name__)

# Enable CORS for all routes and all domains (this solved CORS errors)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type"]}})
USERNAME_NOT_IN_DATA = -1
INCORRECT_PASSWORD = -2

def getUserId(tryUsername, tryPassword):
    # Opens database file
    conn = sqlite3.connect('../../Data/userdata/users.db')  # Ensure this path is correct
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
    conn.close
    
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



# Handles OPTIONS request for CORS preflight, fixes OPTIONS error of pre-post request
@app.route('/login', methods=["OPTIONS"])
def options():
    response = make_response('', 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response



# Handles POST request for login
@app.route('/login', methods=['POST'])
def login():

    print("Login request receieved")

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
        return jsonify({"message": "Error: User does not exist"}), 404
    elif user_id == INCORRECT_PASSWORD:
        return jsonify({"message": "Error: Incorrect password"}), 401

    # Successful login, return user ID or a success message
    return jsonify({"message": "Login successful!", "user_id": user_id}), 200



@app.route('/register', methods=['POST'])
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

    if usernameTaken(username):
        return jsonify({"message":"Error: Username already taken"}), 409
    elif emailTaken(email):
        return jsonify({"message":"Error: Email already taken"}), 409

    hashed_password = hash_password(password)

    addUserToDB(username,email,hashed_password)
    return jsonify({"message": "Working on it"}), 200


#Lets Flask server run
if __name__ == '__main__':
    app.run(debug=True)