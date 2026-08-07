import os
import pandas as pd
from rapidfuzz import process

# Locate dataset automatically
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "dataset", "products.csv")

# Load products
products = pd.read_csv(CSV_PATH)

def search_product(query):
    names = products["name"].tolist()

    results = process.extract(query, names, limit=5)

    recommendations = []

    for item in results:
        product = products[products["name"] == item[0]].iloc[0]

        recommendations.append({
            "id": int(product["id"]),
            "name": product["name"],
            "category": product["category"],
            "price": int(product["price"])
        })

    return recommendations