from flask import Flask, render_template, request, url_for 
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use the PORT environment variable
    app.run(host='0.0.0.0', port=port)

