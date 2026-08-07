from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from recommender import search_product, products

app = Flask(__name__)
app.secret_key = "smartshop123"


@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template(
        "index.html",
        products=products.to_dict(orient="records")
    )


@app.route("/search")
def search():

    query = request.args.get("q", "")

    if query == "":
        return jsonify(products.to_dict(orient="records"))

    return jsonify(search_product(query))


@app.route("/product/<int:pid>")
def product(pid):

    row = products[products["id"] == pid].iloc[0]

    return render_template(
        "product.html",
        product=row.to_dict()
    )


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        if email and password:
            session["user"] = email
            return redirect(url_for("home"))

    return render_template("login.html")

# ---------------- SIGNUP ----------------

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":
        return redirect(url_for("login"))

    return render_template("signup.html")


# ---------------- CART ----------------

@app.route("/add_to_cart/<int:pid>")
def add_to_cart(pid):

    if "cart" not in session:
        session["cart"] = []

    cart = session["cart"]
    cart.append(pid)
    session["cart"] = cart

    return redirect(url_for("cart"))


@app.route("/cart")
def cart():

    cart_ids = session.get("cart", [])

    cart_products = []
    total = 0

    for pid in cart_ids:

        row = products[products["id"] == pid].iloc[0].to_dict()

        cart_products.append(row)

        total += row["price"]

    return render_template(
        "cart.html",
        products=cart_products,
        total=total
    )


@app.route("/remove_from_cart/<int:pid>")
def remove_from_cart(pid):

    cart = session.get("cart", [])

    if pid in cart:
        cart.remove(pid)

    session["cart"] = cart

    return redirect(url_for("cart"))


# ---------------- WISHLIST ----------------

@app.route("/add_to_wishlist/<int:pid>")
def add_to_wishlist(pid):

    if "wishlist" not in session:
        session["wishlist"] = []

    wishlist = session["wishlist"]

    if pid not in wishlist:
        wishlist.append(pid)

    session["wishlist"] = wishlist

    return redirect(url_for("wishlist"))


@app.route("/wishlist")
def wishlist():

    wishlist_ids = session.get("wishlist", [])

    wishlist_products = []

    for pid in wishlist_ids:

        row = products[products["id"] == pid].iloc[0].to_dict()

        wishlist_products.append(row)

    return render_template(
        "wishlist.html",
        products=wishlist_products
    )


@app.route("/remove_from_wishlist/<int:pid>")
def remove_from_wishlist(pid):

    wishlist = session.get("wishlist", [])

    if pid in wishlist:
        wishlist.remove(pid)

    session["wishlist"] = wishlist

    return redirect(url_for("wishlist"))

@app.route("/categories")
def categories():
    return render_template("categories.html")


@app.route("/trending")
def trending():
    return render_template(
        "trending.html",
        products=products.to_dict(orient="records")
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)