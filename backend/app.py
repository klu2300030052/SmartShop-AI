from flask import Flask, render_template, request, jsonify, redirect, url_for, session

from recommender import (
    search_product,
    products,
    detect_intent,
    complete_the_look,
    cold_start_recommendations
)


app = Flask(__name__)
app.secret_key = "smartshop123"


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    if "user" not in session:
        return redirect(url_for("login"))

    recommendations = cold_start_recommendations(10)

    return render_template(
        "index.html",
        products=recommendations
    )


# =========================================================
# AI SEARCH
# =========================================================

@app.route("/search")
def search():

    query = request.args.get("q", "").strip()

    if query == "":
        return jsonify(
            cold_start_recommendations(10)
        )

    return jsonify(
        search_product(query)
    )


# =========================================================
# INTENT DETECTION
# =========================================================

@app.route("/intent")
def intent():

    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({
            "intents": ["general"]
        })

    return jsonify({
        "intents": detect_intent(query)
    })


# =========================================================
# COMPLETE THE LOOK
# =========================================================

@app.route("/complete-look/<int:pid>")
def complete_look(pid):

    return jsonify(
        complete_the_look(pid)
    )


# =========================================================
# PRODUCT
# =========================================================

@app.route("/product/<int:pid>")
def product(pid):

    matching = products[
        products["id"] == pid
    ]

    if matching.empty:
        return "Product not found", 404

    row = matching.iloc[0].to_dict()

    return render_template(
        "product.html",
        product=row
    )


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        if email and password:

            session["user"] = email

            return redirect(
                url_for("home")
            )

    return render_template("login.html")


# =========================================================
# SIGNUP
# =========================================================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":
        return redirect(
            url_for("login")
        )

    return render_template("signup.html")


# =========================================================
# CART
# =========================================================

@app.route("/add_to_cart/<int:pid>")
def add_to_cart(pid):

    if "cart" not in session:
        session["cart"] = []

    cart = session["cart"]

    if pid not in cart:
        cart.append(pid)

    session["cart"] = cart

    return redirect(
        url_for("cart")
    )


@app.route("/cart")
def cart():

    cart_ids = session.get(
        "cart",
        []
    )

    cart_products = []
    total = 0

    for pid in cart_ids:

        matching = products[
            products["id"] == pid
        ]

        if matching.empty:
            continue

        row = matching.iloc[0].to_dict()

        cart_products.append(row)

        total += float(row["price"])

    return render_template(
        "cart.html",
        products=cart_products,
        total=int(total)
    )


@app.route("/remove_from_cart/<int:pid>")
def remove_from_cart(pid):

    cart = session.get(
        "cart",
        []
    )

    if pid in cart:
        cart.remove(pid)

    session["cart"] = cart

    return redirect(
        url_for("cart")
    )


# =========================================================
# WISHLIST
# =========================================================

@app.route("/add_to_wishlist/<int:pid>")
def add_to_wishlist(pid):

    if "wishlist" not in session:
        session["wishlist"] = []

    wishlist = session["wishlist"]

    if pid not in wishlist:
        wishlist.append(pid)

    session["wishlist"] = wishlist

    return redirect(
        url_for("wishlist")
    )


@app.route("/wishlist")
def wishlist():

    wishlist_ids = session.get(
        "wishlist",
        []
    )

    wishlist_products = []

    for pid in wishlist_ids:

        matching = products[
            products["id"] == pid
        ]

        if matching.empty:
            continue

        row = matching.iloc[0].to_dict()

        wishlist_products.append(row)

    return render_template(
        "wishlist.html",
        products=wishlist_products
    )


@app.route("/remove_from_wishlist/<int:pid>")
def remove_from_wishlist(pid):

    wishlist = session.get(
        "wishlist",
        []
    )

    if pid in wishlist:
        wishlist.remove(pid)

    session["wishlist"] = wishlist

    return redirect(
        url_for("wishlist")
    )


# =========================================================
# CATEGORIES
# =========================================================

@app.route("/categories")
def categories():

    return render_template(
        "categories.html"
    )


# =========================================================
# TRENDING
# =========================================================

@app.route("/trending")
def trending():

    trending_products = products.sort_values(
        by="rating",
        ascending=False
    ).head(10)

    return render_template(
        "trending.html",
        products=trending_products.to_dict(
            orient="records"
        )
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)