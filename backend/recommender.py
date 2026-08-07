import os
import pandas as pd
from rapidfuzz import process

# Locate dataset automatically
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "dataset", "products.csv")

# Load products
products = pd.read_csv(CSV_PATH)


def search_product(query):

    # Return all products if search box is empty
    if query.strip() == "":
        return products.to_dict(orient="records")

    # Search by product name + category
    search_list = (
        products["name"] + " " + products["category"]
    ).tolist()

    results = process.extract(
        query,
        search_list,
        limit=10,
        score_cutoff=40
    )

    recommendations = []

    for item in results:

        row = products.iloc[item[2]]

        recommendations.append({
            "id": int(row["id"]),
            "name": row["name"],
            "category": row["category"],
            "price": int(row["price"]),
            "rating": float(row["rating"]),
            "stock": int(row["stock"]),
            "image": str(row["image"])
        })

    return recommendations