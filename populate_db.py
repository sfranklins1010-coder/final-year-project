import os
import django
import random
from datetime import date, timedelta
import random

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_project.settings')
django.setup()

from forecasting.models import Product, SalesHistory
from forecasting.utils import generate_forecast

def populate():
    print("Populating database...")

    # Clear existing data
    SalesHistory.objects.all().delete()
    Product.objects.all().delete()

    products_data = [
        # Electronics
        {"name": "Wireless Mouse", "category": "Electronics", "stock": 150, "price": 25.00},
        {"name": "Mechanical Keyboard", "category": "Electronics", "stock": 45, "price": 80.00},
        {"name": "Gaming Headset", "category": "Electronics", "stock": 80, "price": 60.00},
        {"name": "Webcam 1080p", "category": "Electronics", "stock": 30, "price": 45.00},
        {"name": "Bluetooth Speaker", "category": "Electronics", "stock": 200, "price": 40.00},
        {"name": "Smart Watch Pro", "category": "Electronics", "stock": 15, "price": 199.00},
        {"name": "Noise Cancelling Headphones", "category": "Electronics", "stock": 12, "price": 299.00},
        
        # Accessories
        {"name": "USB-C Cable", "category": "Accessories", "stock": 500, "price": 10.00},
        {"name": "Laptop Stand", "category": "Accessories", "stock": 20, "price": 35.00},
        {"name": "Power Bank 20000mAh", "category": "Accessories", "stock": 60, "price": 30.00},
        {"name": "Laptop Sleeve", "category": "Accessories", "stock": 100, "price": 25.00},
        {"name": "Desk Mat RGB", "category": "Accessories", "stock": 40, "price": 20.00},

        # Smart Home
        {"name": "Smart Bulb RGB", "category": "Smart Home", "stock": 300, "price": 15.00},
        {"name": "Smart Plug Mini", "category": "Smart Home", "stock": 150, "price": 12.00},
        {"name": "Security Camera Outdoor", "category": "Smart Home", "stock": 8, "price": 85.00},
        {"name": "Home Assistant Hub", "category": "Smart Home", "stock": 25, "price": 120.00},

        # Lifestyle & Fitness
        {"name": "Yoga Mat", "category": "Lifestyle", "stock": 60, "price": 30.00},
        {"name": "Adjustable Dumbbells", "category": "Lifestyle", "stock": 5, "price": 150.00},
        {"name": "Resistance Bands Set", "category": "Lifestyle", "stock": 120, "price": 18.00},
        {"name": "Insulated Water Bottle", "category": "Lifestyle", "stock": 250, "price": 22.00},
    ]

    for p_data in products_data:
        product = Product.objects.create(
            name=p_data["name"],
            category=p_data["category"],
            current_stock=p_data["stock"],
            unit_price=p_data["price"]
        )
        
        # Generate Sales History (Last 6 months)
        start_date = date.today() - timedelta(days=180)
        current_date = start_date
        
        # Trend simulation
        trend_factor = random.uniform(0.8, 1.2) 
        
        while current_date < date.today():
            # Random quantity with some seasonality/trend
            base_sales = random.randint(5, 20)
            if p_data["name"] == "Wireless Mouse": # Steady seller
                sales = base_sales + int(current_date.month) 
            elif p_data["name"] == "Laptop Stand": # Low seller
                sales = random.randint(1, 5)
            else:
                sales = int(base_sales * trend_factor)
                
            SalesHistory.objects.create(
                product=product,
                date=current_date,
                quantity_sold=max(0, sales)
            )
            current_date += timedelta(days=random.randint(2, 5)) # Random sales intervals
            
        print(f"Created data for {product.name}")
        
    print("Generating forecasts...")
    from forecasting.utils import train_and_predict_all
    train_and_predict_all()
    print("Done!")

if __name__ == '__main__':
    populate()
