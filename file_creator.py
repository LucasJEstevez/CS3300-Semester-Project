import pandas as pd
import random
# import fsspec

# pip install fsspec

# Data for the cars
years = list(range(1990, 2024))
makes = ['Toyota', 'Honda', 'Ford', 'Chevrolet', 'BMW', 'Mercedes', 'Audi', 'Nissan', 'Volkswagen', 'Hyundai']
models = {
    'Toyota': ['Corolla', 'Camry', 'Prius', 'RAV4', '4Runner', 'Highlander', 'Land Cruiser', 'Tacoma', 'Avalon'],
    'Honda': ['Civic', 'Accord', 'CR-V', 'Pilot', 'HR-V', 'Integra'],
    'Ford': ['Fiesta', 'Mustang', 'Explorer', 'F-150', 'Focus', 'Escape', 'Ranger', 'Taurus'],
    'Chevrolet': ['Malibu', 'Impala', 'Equinox', 'Tahoe', 'Suburban', 'Silverado'],
    'BMW': ['3 Series', '5 Series', 'X5', 'X3'],
    'Mercedes': ['C-Class', 'E-Class', 'GLE', 'GLA', 'S-Class'],
    'Audi': ['A4', 'A6', 'Q5', 'Q7'],
    'Nissan': ['Altima', 'Maxima', 'Rogue', 'Murano', 'Pathfinder', 'Frontier'],
    'Volkswagen': ['Golf', 'Passat', 'Tiguan', 'Atlas', 'Jetta'],
    'Hyundai': ['Elantra', 'Sonata', 'Tucson', 'Santa Fe'],
    'Kia': ['Forte', 'K5', 'Sorento', 'Rio'],
    'Mazda': ['MX5', 'CX-50', 'CX-5', 'CX-90', '3'],
    'Lexus': ['ES300', 'GS', 'GS350', 'ES', 'LS', 'RX'],
    'Subaru': ['Outback', 'Forester', 'WRX'],
    'Jeep': ['Grand Cherokee', 'Wrangler'],
    'Chrysler': ['300'],
    'Volvo': ['XC90'],
    'Acura': ['TL'],
    'Lincoln': ['Navigator'],
    'Dodge': ['Durango'],
    # 'Buick': ['Enclave']
}
trims = ['base','sport','luxury', 'N/A']
doors = ['two-door', 'four-door']
status_options = ['New', 'Certified', 'Used']
purchase_modes = ['Dealership', 'Individual Seller']

# Generate random data
data = []
for _ in range(32):
    make = random.choice(makes)
    model = random.choice(models[make])
    year = random.choice(years)
    trim = random.choice(trims)

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


    # purchase_mode = random.choice(purchase_modes)

    data.append((year, make, model, miles, sale_price, status, purchase_mode))

# Create DataFrame
df = pd.DataFrame(data, columns=['Year', 'Make', 'Model', 'Miles', 'Sale Price', 'Status', 'Mode of Purchase'])

# Save the data to an Excel-like CSV file
file_path = "C://Users//jecam//PycharmProjects//Personal Use//32_cars.csv"
df.to_csv(file_path, index=False)

# file_path
