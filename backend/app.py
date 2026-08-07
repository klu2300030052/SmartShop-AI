from flask import Flask, render_template, request, jsonify
from recommender import search_product, products

app = Flask(__name__)

@app.route("/")
def home():
    product_list = products.to_dict(orient="records")
    return render_template("index.html", products=product_list)

@app.route("/search")
def search():
    query = request.args.get("q", "")

    if query == "":
        return jsonify(products.to_dict(orient="records"))

    results = search_product(query)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)