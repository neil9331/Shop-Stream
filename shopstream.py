"""
ShopStream — an interactive e-commerce demo built with Streamlit.

Run:  streamlit run app.py
All product and review data is simulated (seeded random) for demonstration.
"""
import random
import re
from datetime import date

import streamlit as st

# ----------------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------------
st.set_page_config(page_title="ShopStream", page_icon="🛍️", layout="wide")

CATEGORIES = ["Electronics", "Fashion", "Home", "Toys"]
CATEGORY_ICONS = {"Electronics": "💻", "Fashion": "👗", "Home": "🏠", "Toys": "🧸"}
CATEGORY_COLORS = {"Electronics": "1e3a8a", "Fashion": "9d174d", "Home": "065f46", "Toys": "9a3412"}

# ----------------------------------------------------------------------------
# Custom CSS
# ----------------------------------------------------------------------------
st.markdown(
    """
<style>
:root{
  --accent:#ff4b4b; --accent-2:#ff8a00; --card:#1a1f2b; --card-border:#2a3142;
  --muted:#9aa3b5; --text:#f2f4f8; --sale:#e11d48; --ok:#22c55e;
}
.block-container{padding-top:1.2rem; max-width:1300px;}

/* Navigation bar */
.navbar{display:flex; align-items:center; justify-content:space-between;
  background:linear-gradient(90deg,#111827,#1f2937); padding:14px 24px;
  border-radius:14px; border:1px solid var(--card-border); margin-bottom:14px;}
.brand{font-size:1.6rem; font-weight:800; color:var(--text); letter-spacing:.5px;}
.brand span{background:linear-gradient(90deg,var(--accent),var(--accent-2));
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;}
.nav-links a{color:var(--muted); margin-left:22px; text-decoration:none; font-weight:600;}
.nav-links a:hover{color:var(--text);}
.cart-pill{background:var(--accent); color:#fff; padding:6px 14px; border-radius:999px;
  font-weight:700; margin-left:22px;}

/* Hero */
.hero{background:linear-gradient(120deg,#ff4b4b 0%,#ff8a00 55%,#ffc300 100%);
  border-radius:18px; padding:48px 40px; color:#fff; margin:8px 0 26px 0;
  box-shadow:0 10px 30px rgba(255,75,75,.25);}
.hero h1{font-size:2.6rem; margin:0 0 8px 0; color:#fff; font-weight:800;}
.hero p{font-size:1.15rem; margin:0 0 18px 0; opacity:.95;}
.hero .cta{display:inline-block; background:#111827; color:#fff; padding:10px 22px;
  border-radius:10px; font-weight:700;}
.hero .badge{display:inline-block; background:rgba(255,255,255,.2); padding:4px 12px;
  border-radius:999px; font-size:.85rem; margin-bottom:12px; font-weight:600;}

/* Section titles */
.section-title{font-size:1.6rem; font-weight:800; color:var(--text);
  border-bottom:2px solid var(--card-border); padding-bottom:8px; margin:30px 0 16px 0;}

/* Product card */
.product-card{background:var(--card); border:1px solid var(--card-border);
  border-radius:14px; padding:12px; transition:transform .15s ease, box-shadow .15s ease;
  height:100%;}
.product-card:hover{transform:translateY(-4px); box-shadow:0 10px 24px rgba(0,0,0,.35);}
.product-card img{width:100%; aspect-ratio:1/1; object-fit:cover; border-radius:10px;}
.product-name{font-weight:700; color:var(--text); margin:10px 0 4px 0; font-size:.98rem;}
.product-cat{color:var(--muted); font-size:.78rem; text-transform:uppercase; letter-spacing:.6px;}
.price-row{margin:6px 0; display:flex; align-items:center; gap:8px; flex-wrap:wrap;}
.price{color:var(--accent); font-weight:800; font-size:1.1rem;}
.old-price{color:var(--muted); text-decoration:line-through; font-size:.9rem;}
.sale-badge{background:var(--sale); color:#fff; font-size:.7rem; font-weight:800;
  padding:2px 7px; border-radius:5px;}
.rating{color:#fbbf24; font-size:.9rem;}
.rating span{color:var(--muted); margin-left:4px;}

/* Deal of the day */
.deal{display:flex; gap:28px; align-items:center; background:linear-gradient(120deg,#1e1b4b,#312e81);
  border:1px solid #4338ca; border-radius:18px; padding:26px; flex-wrap:wrap;}
.deal img{width:260px; max-width:100%; border-radius:14px;}
.deal h2{color:#fff; margin:6px 0;}
.deal .big-price{font-size:2.2rem; font-weight:800; color:#fde047;}
.deal .timer{background:rgba(255,255,255,.12); color:#fff; padding:6px 12px;
  border-radius:8px; display:inline-block; font-weight:700; margin-top:8px;}

/* Reviews */
.review{background:var(--card); border:1px solid var(--card-border); border-left:4px solid var(--accent);
  border-radius:12px; padding:16px; height:100%;}
.review .who{font-weight:700; color:var(--text);}
.review .text{color:#d1d5db; font-style:italic; margin:8px 0;}
.review .meta{color:var(--muted); font-size:.8rem;}

/* Newsletter */
.newsletter{background:linear-gradient(120deg,#064e3b,#065f46); border-radius:18px;
  padding:26px 30px; color:#fff; margin-top:10px;}
.newsletter h3{margin:0 0 4px 0; color:#fff;}

.footer{text-align:center; color:var(--muted); padding:30px 0 10px 0; font-size:.85rem;}

/* Buttons */
.stButton>button{border-radius:10px; font-weight:700; width:100%;
  border:1px solid var(--card-border);}
.stButton>button:hover{border-color:var(--accent); color:var(--accent);}

@media (max-width: 768px){
  .hero{padding:30px 22px;} .hero h1{font-size:1.8rem;}
  .nav-links{display:none;}
}
</style>
""",
    unsafe_allow_html=True,
)


# ----------------------------------------------------------------------------
# Simulated data
# ----------------------------------------------------------------------------
ADJECTIVES = ["Smart", "Classic", "Premium", "Eco", "Ultra", "Cozy", "Pro", "Mini"]
NOUNS = {
    "Electronics": ["Headphones", "Smartwatch", "Speaker", "Tablet", "Camera", "Charger"],
    "Fashion": ["Jacket", "Sneakers", "Handbag", "Sunglasses", "Scarf", "Watch"],
    "Home": ["Lamp", "Cushion", "Coffee Maker", "Vase", "Blender", "Rug"],
    "Toys": ["Robot Kit", "Puzzle", "Plush Bear", "Race Car", "Building Blocks", "Drone"],
}


@st.cache_data
def generate_products(n_per_category: int = 8, seed: int = 42):
    rng = random.Random(seed)
    products = []
    pid = 1
    for cat in CATEGORIES:
        for i in range(1, n_per_category + 1):
            price = round(rng.uniform(15, 350), 2)
            discount = rng.choice([0, 0, 0, 10, 15, 20, 25, 30])
            products.append(
                {
                    "id": pid,
                    "name": f"{rng.choice(ADJECTIVES)} {rng.choice(NOUNS[cat])}",
                    "category": cat,
                    "price": price,
                    "discount": discount,
                    "final_price": round(price * (1 - discount / 100), 2),
                    "rating": round(rng.uniform(3.5, 5.0), 1),
                    "reviews": rng.randint(12, 2400),
                    "image": (
                        f"https://placehold.co/400x400/{CATEGORY_COLORS[cat]}/ffffff"
                        f"?text={cat}+{i}&font=raleway"
                    ),
                }
            )
            pid += 1
    return products


@st.cache_data
def generate_reviews(seed: int = 7):
    rng = random.Random(seed)
    names = ["Aisha K.", "Rahul M.", "Sofia L.", "Omar H.", "Emily R.", "Chen W."]
    texts = [
        "Fast delivery and the quality exceeded my expectations!",
        "ShopStream is now my go-to store. Great deals every day.",
        "Customer support was super helpful with my exchange.",
        "Loved the recommendations — found exactly what I needed.",
        "Beautiful packaging, great prices. Highly recommend!",
        "The Deal of the Day saved me a lot. Will shop again.",
    ]
    return [
        {"name": n, "text": t, "stars": rng.randint(4, 5), "city": rng.choice(
            ["Dubai", "Mumbai", "London", "Toronto", "Singapore", "Sydney"])}
        for n, t in zip(names, texts)
    ]


PRODUCTS = generate_products()
REVIEWS = generate_reviews()
BY_ID = {p["id"]: p for p in PRODUCTS}


# ----------------------------------------------------------------------------
# Session state
# ----------------------------------------------------------------------------
st.session_state.setdefault("cart", {})          # {product_id: qty}
st.session_state.setdefault("interests", set())  # categories user interacted with
st.session_state.setdefault("subscribers", [])


def add_to_cart(pid: int):
    cart = st.session_state.cart
    cart[pid] = cart.get(pid, 0) + 1
    st.session_state.interests.add(BY_ID[pid]["category"])
    st.toast(f"Added **{BY_ID[pid]['name']}** to cart 🛒")


def money(x: float) -> str:
    # &#36; instead of "$" so Streamlit's markdown doesn't treat $...$ as LaTeX
    return f"&#36;{x:,.2f}"


def stars(r: float) -> str:
    full = int(round(r))
    return "★" * full + "☆" * (5 - full)


# ----------------------------------------------------------------------------
# Reusable product card
# ----------------------------------------------------------------------------
def product_card(p: dict, key_prefix: str):
    if p["discount"]:
        price_html = (
            f'<span class="sale-badge">-{p["discount"]}%</span>'
            f'<span class="price">{money(p["final_price"])}</span>'
            f'<span class="old-price">{money(p["price"])}</span>'
        )
    else:
        price_html = f'<span class="price">{money(p["price"])}</span>'

    st.markdown(
        f"""
<div class="product-card">
  <img src="{p['image']}" alt="{p['name']}">
  <div class="product-cat">{CATEGORY_ICONS[p['category']]} {p['category']}</div>
  <div class="product-name">{p['name']}</div>
  <div class="price-row">{price_html}</div>
  <div class="rating">{stars(p['rating'])}<span>{p['rating']}/5 · {p['reviews']} reviews</span></div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.button("Add to Cart 🛒", key=f"{key_prefix}_{p['id']}",
              on_click=add_to_cart, args=(p["id"],))


def product_grid(items: list, key_prefix: str, cols: int = 4):
    if not items:
        st.info("No products match your search.")
        return
    for row_start in range(0, len(items), cols):
        columns = st.columns(cols, gap="medium")
        for col, p in zip(columns, items[row_start:row_start + cols]):
            with col:
                product_card(p, key_prefix)


# ----------------------------------------------------------------------------
# Sidebar: cart + filters
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🛒 Your Cart")
    cart = st.session_state.cart
    if not cart:
        st.caption("Your cart is empty.")
    else:
        total = 0.0
        for pid, qty in list(cart.items()):
            p = BY_ID[pid]
            line = p["final_price"] * qty
            total += line
            c1, c2 = st.columns([4, 1])
            c1.markdown(f"**{p['name']}** × {qty}  \n{money(line)}", unsafe_allow_html=True)
            if c2.button("✕", key=f"rm_{pid}"):
                del cart[pid]
                st.rerun()
        st.markdown(f"### Total: {money(total)}", unsafe_allow_html=True)
        if st.button("Checkout"):
            st.success("Order placed! (demo — no payment processed)")
            st.session_state.cart = {}

    st.divider()
    st.markdown("## 🔎 Filters")
    price_range = st.slider("Price range ($)", 0, 400, (0, 400), step=10)
    min_rating = st.slider("Minimum rating", 3.5, 5.0, 3.5, step=0.1)
    sort_by = st.selectbox("Sort by", ["Featured", "Price: Low → High",
                                       "Price: High → Low", "Top Rated", "Biggest Discount"])


def apply_filters(items):
    items = [p for p in items
             if price_range[0] <= p["final_price"] <= price_range[1]
             and p["rating"] >= min_rating]
    if sort_by == "Price: Low → High":
        items.sort(key=lambda p: p["final_price"])
    elif sort_by == "Price: High → Low":
        items.sort(key=lambda p: -p["final_price"])
    elif sort_by == "Top Rated":
        items.sort(key=lambda p: -p["rating"])
    elif sort_by == "Biggest Discount":
        items.sort(key=lambda p: -p["discount"])
    return items


# ----------------------------------------------------------------------------
# Navbar
# ----------------------------------------------------------------------------
cart_count = sum(st.session_state.cart.values())
st.markdown(
    f"""
<div class="navbar">
  <div class="brand">🛍️ Shop<span>Stream</span></div>
  <div class="nav-links">
    <a href="#featured-products">Featured</a>
    <a href="#deal-of-the-day">Deals</a>
    <a href="#shop-by-category">Categories</a>
    <a href="#what-our-customers-say">Reviews</a>
    <span class="cart-pill">🛒 {cart_count}</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# Search bar
search = st.text_input("Search", placeholder="🔍  Search products, e.g. 'headphones' or 'toys'…",
                       label_visibility="collapsed")

if search.strip():
    q = search.strip().lower()
    results = [p for p in PRODUCTS if q in p["name"].lower() or q in p["category"].lower()]
    for p in results:
        st.session_state.interests.add(p["category"])
    st.markdown(f'<div class="section-title">Search results for "{search}"</div>',
                unsafe_allow_html=True)
    product_grid(apply_filters(results), "search")

# ----------------------------------------------------------------------------
# Hero
# ----------------------------------------------------------------------------
st.markdown(
    """
<div class="hero">
  <div class="badge">🔥 MEGA SALE · Limited time</div>
  <h1>Shop Smarter. Live Better.</h1>
  <p>Up to 30% off across Electronics, Fashion, Home &amp; Toys. Free shipping on orders over &#36;50.</p>
  <span class="cta">Start Shopping →</span>
</div>
""",
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Featured products (one or two from each category, stable per day)
# ----------------------------------------------------------------------------
st.markdown('<div class="section-title" id="featured-products">⭐ Featured Products</div>',
            unsafe_allow_html=True)
day_rng = random.Random(date.today().toordinal())
featured = [day_rng.choice([p for p in PRODUCTS if p["category"] == c]) for c in CATEGORIES]
product_grid(featured, "featured")

# ----------------------------------------------------------------------------
# Deal of the day
# ----------------------------------------------------------------------------
st.markdown('<div class="section-title" id="deal-of-the-day">⚡ Deal of the Day</div>',
            unsafe_allow_html=True)
deal_base = day_rng.choice(PRODUCTS)
deal = dict(deal_base, discount=40, final_price=round(deal_base["price"] * 0.6, 2))
d1, d2 = st.columns([3, 1])
with d1:
    st.markdown(
        f"""
<div class="deal">
  <img src="{deal['image']}" alt="{deal['name']}">
  <div>
    <span class="sale-badge">40% OFF TODAY</span>
    <h2>{deal['name']}</h2>
    <div class="product-cat" style="color:#c7d2fe">{deal['category']}</div>
    <div class="big-price">{money(deal['final_price'])}
      <span class="old-price" style="font-size:1.1rem">{money(deal['price'])}</span></div>
    <div class="rating">{stars(deal['rating'])}<span style="color:#c7d2fe">{deal['rating']}/5</span></div>
    <div class="timer">⏰ Ends at midnight</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
with d2:
    st.write("")
    st.metric("You save", f"${deal['price'] - deal['final_price']:,.2f}", "-40%")
    if st.button("Grab the Deal 🛒", key="deal_btn", type="primary"):
        BY_ID[deal["id"]] = deal  # use the deal price for this item in the cart
        add_to_cart(deal["id"])

# ----------------------------------------------------------------------------
# Catalog by category
# ----------------------------------------------------------------------------
st.markdown('<div class="section-title" id="shop-by-category">🗂️ Shop by Category</div>',
            unsafe_allow_html=True)
tabs = st.tabs([f"{CATEGORY_ICONS[c]} {c}" for c in CATEGORIES])
for tab, cat in zip(tabs, CATEGORIES):
    with tab:
        product_grid(apply_filters([p for p in PRODUCTS if p["category"] == cat]), f"cat_{cat}")

# ----------------------------------------------------------------------------
# Recommendations
# ----------------------------------------------------------------------------
st.markdown('<div class="section-title">🎯 Recommended for You</div>', unsafe_allow_html=True)
chosen = st.multiselect("What are you interested in?", CATEGORIES,
                        default=sorted(st.session_state.interests))
interest = set(chosen) or set(CATEGORIES)
if chosen:
    st.caption(f"Based on your interest in {', '.join(chosen)}.")
else:
    st.caption("Pick a category or add items to your cart to personalise these. Showing top-rated picks.")
pool = [p for p in PRODUCTS if p["category"] in interest and p["id"] not in st.session_state.cart]
recs = sorted(pool, key=lambda p: (-p["rating"], -p["discount"]))[:4]
product_grid(recs, "rec")

# ----------------------------------------------------------------------------
# Featured video
# ----------------------------------------------------------------------------
st.markdown('<div class="section-title">🎬 Featured Video</div>', unsafe_allow_html=True)
v1, v2 = st.columns([2, 1])
with v1:
    st.video("https://www.youtube.com/watch?v=aqz-KE-bpKQ")  # placeholder promo (Big Buck Bunny, CC-BY)
with v2:
    st.markdown("### The ShopStream Season Launch")
    st.write("Get a first look at this season's collections, curated by our style and tech teams. "
             "New arrivals drop every Friday.")
    st.markdown("- 🚚 Free shipping over $50\n- ↩️ 30-day easy returns\n- 🔒 Secure checkout")

# ----------------------------------------------------------------------------
# Reviews & testimonials
# ----------------------------------------------------------------------------
st.markdown('<div class="section-title" id="what-our-customers-say">💬 What Our Customers Say</div>',
            unsafe_allow_html=True)
for row in range(0, len(REVIEWS), 3):
    cols = st.columns(3, gap="medium")
    for col, r in zip(cols, REVIEWS[row:row + 3]):
        col.markdown(
            f"""
<div class="review">
  <div class="rating">{stars(r['stars'])}</div>
  <div class="text">“{r['text']}”</div>
  <div class="who">{r['name']}</div>
  <div class="meta">Verified buyer · {r['city']}</div>
</div>
""",
            unsafe_allow_html=True,
        )
    st.write("")

# ----------------------------------------------------------------------------
# Newsletter
# ----------------------------------------------------------------------------
st.markdown(
    """
<div class="newsletter">
  <h3>📬 Join the ShopStream newsletter</h3>
  <div>Exclusive deals, early access to sales and new arrivals — straight to your inbox.</div>
</div>
""",
    unsafe_allow_html=True,
)
with st.form("newsletter", clear_on_submit=True):
    n1, n2 = st.columns([4, 1])
    email = n1.text_input("Email", placeholder="you@example.com", label_visibility="collapsed")
    submitted = n2.form_submit_button("Subscribe")
    if submitted:
        if re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email or ""):
            if email.lower() in st.session_state.subscribers:
                st.info("You're already subscribed! 💌")
            else:
                st.session_state.subscribers.append(email.lower())
                st.success(f"Thanks! {email} is now subscribed. 🎉")
        else:
            st.error("Please enter a valid email address.")

st.markdown(
    '<div class="footer">© 2026 ShopStream · Demo store with simulated data · Built with Streamlit</div>',
    unsafe_allow_html=True,
)
