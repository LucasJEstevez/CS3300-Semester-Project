import pandas as pd
import random

# Data for the cars
years = list(range(1995, 2024))
# Define cars that will appear as available/sold as a dictionary
makes = ['Toyota', 'Honda', 'Ford', 'Chevrolet', 'BMW', 'Mercedes', 'Audi', 'Nissan', 'Volkswagen', 'Hyundai', 'Kia',
         'Buick', 'Mazda', 'Lexus', 'Subaru', 'Jeep', 'Chrysler', 'Volvo', 'Acura', 'Lincoln', 'Dodge', 'GMC']
models = {
    'Toyota': ['Corolla', 'Camry', 'Prius', 'RAV4', '4Runner', 'Highlander', 'Land Cruiser', 'Tacoma', 'Avalon'],
    'Honda': ['Civic', 'Accord', 'CR-V', 'Pilot', 'HR-V'],
    'Ford': ['Fiesta', 'Mustang', 'Explorer', 'F-150', 'Focus', 'Escape', 'Ranger', 'Taurus'],
    'Chevrolet': ['Malibu', 'Impala', 'Equinox', 'Tahoe', 'Suburban', 'Silverado'],
    'BMW': ['3 Series', '5 Series', 'X5', 'X3'],
    'Mercedes': ['C-Class', 'E-Class', 'GLE', 'GLA', 'S-Class'],
    'Audi': ['A3', 'A4', 'A6', 'Q5', 'Q7'],
    'Nissan': ['Altima', 'Maxima', 'Rogue', 'Murano', 'Pathfinder', 'Frontier'],
    'Volkswagen': ['Golf', 'Passat', 'Tiguan', 'Atlas', 'Jetta'],
    'Hyundai': ['Elantra', 'Sonata', 'Tucson', 'Santa Fe'],
    'Kia': ['Forte', 'K5', 'Sorento', 'Rio', 'Sportage'],
    'Mazda': ['MX5', 'CX-50', 'CX-5', 'CX-90', '3'],
    'Lexus': ['ES300', 'GS', 'GS350', 'ES', 'LS', 'RX'],
    'Subaru': ['Outback', 'Forester', 'WRX'],
    'Jeep': ['Grand Cherokee', 'Wrangler'],
    'Chrysler': ['300', 'Town & Country'],
    'Volvo': ['XC90', 'S70', 'S60', ],
    'Acura': ['TL', 'Integra'],
    'Lincoln': ['Navigator'],
    'Dodge': ['Durango', 'Charger', 'Grand Caravan', 'Ram 1500'],
    'Buick': ['LaCrosse', 'Regal'],
    'GMC': ['Sierra', 'Yukon', 'Envoy']
}
trims = ['base', 'sport', 'luxury', 'N/A']
# doors = ['two-door', 'four-door']
status_options = ['New', 'Certified', 'Used']
purchase_modes = ['Dealership', 'Individual Seller']
vehicle_id = 1
# list to have cars appended to
data = []
# Tells the program how many cars to create
for _ in range(15000):
    # Generate random data
    vehicle_id = vehicle_id
    make = random.choice(makes)
    model = random.choice(models[make])
    year = random.choice(years)
    zip_code = random.randint(10000, 99999)
    trim = ""

    # Set vehicle status (new, used, certified)
    if year < 2022:
        if (2018 <= year <= 2022):
            status = 'Certified'
        else:
            status = 'Used'
    else:
        status = 'New'

    # Generate miles and price based on the year and status
    if status == 'New':
        miles = random.randint(0, 100)
        purchase_mode = purchase_modes[0]
        sale_price = random.randint(20000, 50000)
    elif status == 'Certified':
        miles = random.randint(5000, 35000)
        purchase_mode = purchase_modes[0]
        if miles > 20000:
            sale_price = random.randint(10000, 25000)
        else:
            sale_price = random.randint(15000, 35000)
    else:
        miles = random.randint(10000, 150000)
        purchase_mode = random.choice(purchase_modes)
        if purchase_mode == 'Dealership':
            if miles >= 75000:
                sale_price = random.randint(5000, 20000)
            elif 30000 <= miles < 75000:
                sale_price = random.randint(10000, 35000)
            else:
                sale_price = random.randint(10000, 40000)
        else:
            if miles >= 75000:
                sale_price = random.randint(5000, 17500)
            elif 30000 <= miles < 75000:
                sale_price = random.randint(7500, 27500)
            else:
                sale_price = random.randint(7500, 35000)

    # Set vehicle trim level (only applicable to cars newer than 2005 for more realistic cars)
    if year > 2005:
        random_num = random.randint(0, 10000)
        if random_num < 5000:
            trim = trims[0]
        elif 5000 <= random_num <= 8500:
            trim = trims[1]
        elif random_num > 8500:
            trim = trims[2]
    else:
        trim = trims[3]

    # Add randomized vehicle data to list
    data.append((vehicle_id, year, make, model, trim, miles, sale_price, status, purchase_mode, zip_code))
    vehicle_id += 1

# Create DataFrame from list
df = pd.DataFrame(data, columns=['Vehicle_ID', 'Year', 'Make', 'Model', 'Trim', 'Miles', 'Sold For', 'Status', 'Sold By', 'Zip Code Sold'])

# Save the DataFrame to a CSV file
file_path = "C://Users//jecam//PycharmProjects//Personal Use//site_sold_cars.csv"
df.to_csv(file_path, index=False)