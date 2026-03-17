"""Generate a realistic sample e-commerce dataset."""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random, uuid

random.seed(42); np.random.seed(42)

products = ["Wireless Headphones","Running Shoes","Smart Watch","Coffee Maker",
            "Yoga Mat","Laptop Stand","Bluetooth Speaker","Water Bottle",
            "Desk Lamp","Phone Case"]
regions = ["North","South","East","West"]
customers = [str(uuid.uuid4())[:8] for _ in range(500)]
start_date = datetime(2024, 1, 1)

rows = []
for i in range(5000):
    region = random.choice(regions)
    # North has lower sales in Q4 to create the insight
    base_sales = {"North": 45, "South": 85, "East": 70, "West": 60}[region]
    date = start_date + timedelta(days=random.randint(0, 364))
    if region == "North" and date.month >= 10:
        base_sales *= 0.6  # simulate Q4 drop
    rows.append({
        "order_id": str(uuid.uuid4())[:12],
        "product": random.choice(products),
        "sales": round(max(5, np.random.normal(base_sales, 20)), 2),
        "region": region,
        "customer_id": random.choice(customers),
        "date": date.strftime("%Y-%m-%d"),
        "quantity": random.randint(1, 5)
    })

df = pd.DataFrame(rows)
df.to_csv("sample_dataset.csv", index=False)
print(f"Generated {len(df)} rows → sample_dataset.csv")
