from flask import Flask, render_template, request, url_for, jsonify, make_response
import requests
import os
import jinja2

app = Flask(__name__)

def construct_url(car_info, key):
    url = f"https://mc-api.marketcheck.com/v2/predict/car/price?api_key={key}&car_type=used"
    
    vin = car_info.get('vin', None)
    if vin:
        url += f"&vin={car_info['vin']}&miles={car_info['miles1']}"
    else:
        url += f"&miles={car_info['miles2']}&year={car_info['year']}&make={car_info['make']}&model={car_info['model']}&trim={car_info['trim']}"

    return url

def get_car_prediction(car_info, key, url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/price_prediction', methods=['POST'])
def price_prediction():
    car_info = {
        'vin': request.form.get('vin', None),
        'miles1': request.form.get('miles1', None),
        'year': request.form.get('year', None),
        'make': request.form.get('make', None),
        'model': request.form.get('model', None),
        'trim': request.form.get('trim', None),
        'miles2': request.form.get('miles2', None),
    }

    key = os.environ.get('API_KEY')  # Ensure your API key is set as an environment variable
    url = construct_url(car_info, key)
    prediction = get_car_prediction(car_info, key, url)

    if prediction:
        return render_template('results.html', prediction=prediction)
    else:
        return render_template('error.html', message="Failed to retrieve prediction.")
   
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

@app.route('/register')
def register_page():
    return render_template('User_Pages/register.html')

@app.route('/sign-in')
def sign_in_page():
    return render_template('User_Pages/sign-in.html')

@app.route('/buy3')
def buy_three_page():
    return render_template('Sidebar_Pages/buypage3.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use the PORT environment variable
    app.run(host='0.0.0.0', port=port)

# Handles POST request for login
@app.route('/login', methods=['POST'])
def login():

    print("Login request receieved")
    return jsonify({"message":"Login request received"})

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