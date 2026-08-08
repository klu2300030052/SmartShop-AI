import os
import re
import pandas as pd
from rapidfuzz import process, fuzz


# =========================================================
# AI LIBRARIES
# =========================================================

try:
    import faiss
    from sentence_transformers import SentenceTransformer

    AI_AVAILABLE = True

except ImportError:
    AI_AVAILABLE = False


# =========================================================
# DATASET
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

CSV_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "products.csv"
)

products = pd.read_csv(CSV_PATH)


# Make sure important columns have correct types

products["id"] = products["id"].astype(int)
products["price"] = products["price"].astype(float)
products["rating"] = products["rating"].astype(float)
products["stock"] = products["stock"].astype(int)


# =========================================================
# SEARCH TEXT
# =========================================================

products["search_text"] = (
    products["name"].fillna("").astype(str)
    + " "
    + products["category"].fillna("").astype(str)
)


# =========================================================
# SENTENCE TRANSFORMER + FAISS
# =========================================================

model = None
index = None


if AI_AVAILABLE:

    try:

        model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        embeddings = model.encode(
            products["search_text"].tolist(),
            normalize_embeddings=True
        )

        dimension = embeddings.shape[1]

        index = faiss.IndexFlatIP(
            dimension
        )

        index.add(embeddings)

        print("AI semantic search enabled.")
        print("FAISS vector index created.")

    except Exception as e:

        print(
            "AI model could not be loaded:",
            e
        )

        model = None
        index = None


# =========================================================
# PRODUCT FORMATTER
# =========================================================

def product_to_dict(row, reason=None):

    product = {
        "id": int(row["id"]),
        "name": str(row["name"]),
        "category": str(row["category"]),
        "price": int(row["price"]),
        "rating": float(row["rating"]),
        "stock": int(row["stock"]),
        "image": str(row["image"])
    }

    if reason:
        product["reason"] = reason

    return product


# =========================================================
# MULTI-INTENT DETECTION
# =========================================================

def detect_intent(query):

    q = query.lower()

    intents = []

    # ---------------- PRICE ----------------

    if any(word in q for word in [
        "cheap",
        "budget",
        "affordable",
        "low price",
        "under",
        "discount",
        "bargain",
        "low cost",
        "cheapest"
    ]):

        intents.append("bargain")


    # ---------------- SPORTS ----------------

    if any(word in q for word in [
        "running",
        "sports",
        "sport",
        "gym",
        "fitness",
        "workout",
        "athletic"
    ]):

        intents.append("sports")


    # ---------------- FASHION ----------------

    if any(word in q for word in [
        "match",
        "matching",
        "outfit",
        "dress",
        "look",
        "wear",
        "fashion",
        "style"
    ]):

        intents.append("fashion")


    # ---------------- ELECTRONICS ----------------

    if any(word in q for word in [
        "phone",
        "mobile",
        "laptop",
        "computer",
        "watch",
        "headphone",
        "headphones",
        "speaker",
        "tablet"
    ]):

        intents.append("electronics")


    # ---------------- GIFT ----------------

    if any(word in q for word in [
        "gift",
        "present",
        "birthday",
        "anniversary"
    ]):

        intents.append("gift")


    if not intents:
        intents.append("general")


    return intents


# =========================================================
# PRODUCT CATEGORY DETECTION
# =========================================================

def detect_category(query):

    q = query.lower()

    # Shoes

    if any(word in q for word in [
        "shoe",
        "shoes",
        "sneaker",
        "sneakers",
        "footwear",
        "running shoe",
        "sports shoe"
    ]):

        return "shoes"


    # Laptops

    if any(word in q for word in [
        "laptop",
        "notebook"
    ]):

        return "laptops"


    # Mobiles

    if any(word in q for word in [
        "phone",
        "mobile",
        "smartphone",
        "iphone",
        "android"
    ]):

        return "mobiles"


    # Headphones

    if any(word in q for word in [
        "headphone",
        "headphones",
        "earphone",
        "earphones",
        "earbuds"
    ]):

        return "headphones"


    # Watches

    if any(word in q for word in [
        "watch",
        "smartwatch"
    ]):

        return "watches"


    # Clothing

    if any(word in q for word in [
        "shirt",
        "tshirt",
        "t-shirt",
        "hoodie",
        "jeans",
        "dress",
        "clothing",
        "jacket"
    ]):

        return "clothing"


    # Bags

    if any(word in q for word in [
        "bag",
        "backpack",
        "luggage"
    ]):

        return "bags"


    # Accessories

    if any(word in q for word in [
        "sunglasses",
        "glasses",
        "accessory",
        "accessories"
    ]):

        return "accessories"


    # Speakers

    if any(word in q for word in [
        "speaker",
        "speakers"
    ]):

        return "speakers"


    return None


# =========================================================
# INTENT SCORE
# =========================================================

def intent_score(row, intents):

    score = 0

    name = str(row["name"]).lower()
    category = str(row["category"]).lower()


    for intent in intents:

        # ---------------- SPORTS ----------------

        if intent == "sports":

            if (
                "sport" in name
                or "running" in name
                or "athletic" in name
                or category == "shoes"
            ):

                score += 5


        # ---------------- ELECTRONICS ----------------

        elif intent == "electronics":

            if category in [
                "mobiles",
                "laptops",
                "headphones",
                "speakers",
                "watches"
            ]:

                score += 5


        # ---------------- FASHION ----------------

        elif intent == "fashion":

            if category in [
                "clothing",
                "shoes",
                "bags",
                "accessories"
            ]:

                score += 5


        # ---------------- GIFT ----------------

        elif intent == "gift":

            if float(row["rating"]) >= 4.5:

                score += 3


        # ---------------- BARGAIN ----------------

        elif intent == "bargain":

            price = float(row["price"])

            if price <= 5000:

                score += 4

            elif price <= 10000:

                score += 1


    return score


# =========================================================
# CATEGORY MATCH SCORE
# =========================================================

def category_score(row, detected_category):

    if not detected_category:

        return 0

    category = str(
        row["category"]
    ).lower()

    name = str(
        row["name"]
    ).lower()


    # Exact category match

    if category == detected_category:

        return 20


    # Product name contains category keyword

    if detected_category.rstrip("s") in name:

        return 12


    # Common variations

    if detected_category == "shoes":

        if any(x in name for x in [
            "shoe",
            "sneaker",
            "footwear"
        ]):

            return 15


    if detected_category == "laptops":

        if "laptop" in name:

            return 15


    if detected_category == "mobiles":

        if any(x in name for x in [
            "phone",
            "mobile"
        ]):

            return 15


    if detected_category == "headphones":

        if any(x in name for x in [
            "headphone",
            "earphone",
            "earbuds"
        ]):

            return 15


    return 0


# =========================================================
# DIVERSITY GUARDRAIL
# =========================================================

def apply_diversity(results, limit=10):

    selected = []

    category_counts = {}

    max_per_category = max(
        1,
        int(limit * 0.35)
    )


    for row in results:

        category = str(
            row["category"]
        )

        count = category_counts.get(
            category,
            0
        )


        if count >= max_per_category:

            continue


        selected.append(row)

        category_counts[category] = (
            count + 1
        )


        if len(selected) >= limit:

            break


    return selected


# =========================================================
# SEMANTIC SEARCH
# =========================================================

def semantic_search(query, limit=20):

    if model is None or index is None:

        return []


    try:

        query_embedding = model.encode(
            [query],
            normalize_embeddings=True
        )


        scores, indices = index.search(
            query_embedding,
            limit
        )


        results = []


        for score, idx in zip(
            scores[0],
            indices[0]
        ):

            if idx < 0:
                continue


            row = products.iloc[
                int(idx)
            ]


            results.append({
                "row": row,
                "score": float(score)
            })


        return results


    except Exception as e:

        print(
            "Semantic search error:",
            e
        )

        return []


# =========================================================
# MAIN AI SEARCH
# =========================================================

def search_product(query):

    query = str(
        query
    ).strip()


    # =====================================================
    # EMPTY SEARCH
    # =====================================================

    if query == "":

        sorted_products = products.sort_values(
            by=["rating", "stock"],
            ascending=[False, False]
        )


        rows = apply_diversity(
            [
                product_to_dict(row)
                for _, row
                in sorted_products.iterrows()
            ],
            limit=10
        )


        return rows


    # =====================================================
    # UNDERSTAND QUERY
    # =====================================================

    intents = detect_intent(
        query
    )

    detected_category = detect_category(
        query
    )


    results = []


    # =====================================================
    # SEMANTIC AI SEARCH
    # =====================================================

    semantic_results = semantic_search(
        query,
        limit=20
    )


    for item in semantic_results:

        row = item["row"]

        semantic_score = item["score"]


        intent_bonus = intent_score(
            row,
            intents
        )


        category_bonus = category_score(
            row,
            detected_category
        )


        final_score = (
            semantic_score * 10
            + intent_bonus
            + category_bonus
            + float(row["rating"]) * 0.2
        )


        results.append({
            "row": row,
            "score": final_score
        })


    # =====================================================
    # RAPIDFUZZ HYBRID SEARCH
    # =====================================================

    search_list = products[
        "search_text"
    ].tolist()


    fuzzy_results = process.extract(
        query,
        search_list,
        scorer=fuzz.WRatio,
        limit=15,
        score_cutoff=30
    )


    for match in fuzzy_results:

        row_index = match[2]

        fuzzy_score = match[1]


        row = products.iloc[
            row_index
        ]


        intent_bonus = intent_score(
            row,
            intents
        )


        category_bonus = category_score(
            row,
            detected_category
        )


        final_score = (
            fuzzy_score / 10
            + intent_bonus
            + category_bonus
            + float(row["rating"]) * 0.2
        )


        results.append({
            "row": row,
            "score": final_score
        })


    # =====================================================
    # REMOVE DUPLICATES
    # =====================================================

    unique = {}


    for item in results:

        pid = int(
            item["row"]["id"]
        )


        if pid not in unique:

            unique[pid] = item


        elif item["score"] > unique[pid]["score"]:

            unique[pid] = item


    # =====================================================
    # SORT RESULTS
    # =====================================================

    ranked = sorted(
        unique.values(),
        key=lambda x: x["score"],
        reverse=True
    )


    # =====================================================
    # STRICT CATEGORY PRIORITY
    # =====================================================

    if detected_category:

        matching = []

        other = []


        for item in ranked:

            row = item["row"]


            score = category_score(
                row,
                detected_category
            )


            if score >= 15:

                matching.append(item)

            else:

                other.append(item)


        # Put exact category products first

        ranked = matching + other


    # =====================================================
    # FORMAT RESULTS
    # =====================================================

    formatted = []


    for item in ranked:

        row = item["row"]


        # Default reason

        reason = (
            "Matched using AI semantic search"
        )


        # Category-specific explanations

        if detected_category:

            if category_score(
                row,
                detected_category
            ) >= 15:

                reason = (
                    "Matched your "
                    + detected_category
                    + " search"
                )


        if "bargain" in intents:

            if float(row["price"]) <= 5000:

                reason = (
                    "Budget-friendly option "
                    "for your search"
                )


        if "sports" in intents:

            reason = (
                "Recommended for your "
                "sports-related intent"
            )


        if "fashion" in intents:

            reason = (
                "Recommended for your "
                "fashion and matching intent"
            )


        if "electronics" in intents:

            reason = (
                "Recommended for your "
                "electronics search"
            )


        if "gift" in intents:

            reason = (
                "Recommended as a "
                "highly rated gift option"
            )


        formatted.append(
            product_to_dict(
                row,
                reason
            )
        )


    # =====================================================
    # FINAL DIVERSITY GUARDRAIL
    # =====================================================

    return apply_diversity(
        formatted,
        limit=10
    )


# =========================================================
# COMPLETE THE LOOK
# =========================================================

def complete_the_look(product_id):

    try:

        row = products[
            products["id"] == int(product_id)
        ].iloc[0]


    except IndexError:

        return []


    category = str(
        row["category"]
    ).lower()


    complementary_categories = {

        "shoes": [
            "clothing",
            "bags",
            "accessories"
        ],

        "clothing": [
            "shoes",
            "bags",
            "accessories"
        ],

        "bags": [
            "clothing",
            "shoes",
            "accessories"
        ],

        "accessories": [
            "clothing",
            "shoes",
            "bags"
        ],

        "mobiles": [
            "headphones",
            "watches",
            "bags"
        ],

        "laptops": [
            "bags",
            "headphones"
        ]
    }


    categories = complementary_categories.get(
        category,
        []
    )


    candidates = products[
        products["category"]
        .str.lower()
        .isin(categories)
    ]


    candidates = candidates.sort_values(
        by="rating",
        ascending=False
    )


    return [
        product_to_dict(
            item,
            "Complements your selected product"
        )
        for _, item
        in candidates.head(5).iterrows()
    ]


# =========================================================
# COLD START
# =========================================================

def cold_start_recommendations(
    limit=10
):

    ranked = products.sort_values(
        by=["rating", "stock"],
        ascending=[False, False]
    )


    formatted = [

        product_to_dict(
            row,
            "Popular choice for new shoppers"
        )

        for _, row
        in ranked.iterrows()

    ]


    return apply_diversity(
        formatted,
        limit
    )