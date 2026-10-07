import streamlit as st
import json
import os
import uuid
import hashlib
from datetime import datetime
import pandas as pd

# ============================================================
# ENZO SMART ORDER - STREAMLIT DEMO
# ============================================================

st.set_page_config(
    page_title="Enzo Smart Order",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# FILE STORAGE / MEMORY
# ============================================================

DATA_FILE = "enzo_data.json"

DEFAULT_DATA = {
    "users": [
        {
            "id": "U001",
            "name": "Demo Customer",
            "email": "customer@vit.ac.in",
            "password": hashlib.sha256("1234".encode()).hexdigest(),
            "role": "customer"
        },
        {
            "id": "S001",
            "name": "Enzo Staff",
            "email": "staff@enzo.com",
            "password": hashlib.sha256("1234".encode()).hexdigest(),
            "role": "staff"
        },
        {
            "id": "A001",
            "name": "Enzo Manager",
            "email": "admin@enzo.com",
            "password": hashlib.sha256("1234".encode()).hexdigest(),
            "role": "admin"
        }
    ],

    "products": [
        {
            "id": "P001",
            "name": "Chicken Burger",
            "category": "Food",
            "price": 80,
            "stock": 20,
            "low_stock": 5,
            "available": True
        },
        {
            "id": "P002",
            "name": "Veg Sandwich",
            "category": "Food",
            "price": 60,
            "stock": 12,
            "low_stock": 5,
            "available": True
        },
        {
            "id": "P003",
            "name": "French Fries",
            "category": "Food",
            "price": 50,
            "stock": 25,
            "low_stock": 5,
            "available": True
        },
        {
            "id": "P004",
            "name": "Coke",
            "category": "Drinks",
            "price": 40,
            "stock": 30,
            "low_stock": 8,
            "available": True
        },
        {
            "id": "P005",
            "name": "Orange Juice",
            "category": "Drinks",
            "price": 50,
            "stock": 15,
            "low_stock": 5,
            "available": True
        },
        {
            "id": "P006",
            "name": "Lays",
            "category": "Snacks",
            "price": 20,
            "stock": 40,
            "low_stock": 10,
            "available": True
        },
        {
            "id": "P007",
            "name": "Pen",
            "category": "Stationery",
            "price": 10,
            "stock": 50,
            "low_stock": 10,
            "available": True
        }
    ],

    "orders": []
}


def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA.copy()

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA.copy()


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


data = load_data()


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "page" not in st.session_state:
    st.session_state.page = "Home"


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def generate_order_id():
    number = 247 + len(data["orders"])
    return f"E{number}"


def generate_pin():
    return str(uuid.uuid4().int)[-4:]


def get_product(product_id):
    for product in data["products"]:
        if product["id"] == product_id:
            return product
    return None


def get_user_orders():
    if not st.session_state.user:
        return []

    email = st.session_state.user["email"]

    return [
        order for order in data["orders"]
        if order["customer_email"] == email
    ]


def order_total(order):
    return sum(
        item["price"] * item["quantity"]
        for item in order["items"]
    )


def status_badge(status):
    badges = {
        "PLACED": "🔵",
        "PAYMENT VERIFIED": "💳",
        "ACCEPTED": "🟡",
        "PREPARING": "🟠",
        "READY": "🟢",
        "PICKUP VERIFIED": "🔐",
        "COMPLETED": "✅",
        "CANCELLED": "❌"
    }

    return f"{badges.get(status, '⚪')} {status}"


def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.cart = {}
    st.rerun()


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 800;
}

.card {
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #ddd;
    margin-bottom: 15px;
}

.price {
    font-size: 22px;
    font-weight: bold;
}

.small {
    color: #777;
}

.big-status {
    font-size: 28px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state.logged_in:

    st.markdown(
        '<div class="main-title">🍔 ENZO SMART ORDER</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Order from anywhere • Pay online • Come when ready • Quick pickup"
    )

    st.divider()

    login_tab, register_tab = st.tabs(
        ["🔐 Sign In", "📝 New Customer"]
    )

    # ---------------- LOGIN ----------------

    with login_tab:

        st.subheader("Sign in")

        email = st.text_input(
            "Email",
            placeholder="Enter your email"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "Sign In",
            type="primary",
            use_container_width=True
        ):

            password_hash = hash_password(password)

            user = next(
                (
                    u for u in data["users"]
                    if u["email"].lower() == email.lower()
                    and u["password"] == password_hash
                ),
                None
            )

            if user:

                st.session_state.logged_in = True
                st.session_state.user = user

                st.success("Login successful!")
                st.rerun()

            else:

                st.error("Invalid email or password.")

        st.info(
            "Demo accounts:\n\n"
            "Customer: customer@vit.ac.in / 1234\n\n"
            "Staff: staff@enzo.com / 1234\n\n"
            "Management: admin@enzo.com / 1234"
        )

    # ---------------- REGISTER ----------------

    with register_tab:

        st.subheader("Create customer account")

        new_name = st.text_input("Name")
        new_email = st.text_input("VIT Email")
        new_password = st.text_input(
            "Create Password",
            type="password"
        )

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            if not new_name or not new_email or not new_password:
                st.warning("Please fill all fields.")

            elif any(
                u["email"].lower() == new_email.lower()
                for u in data["users"]
            ):
                st.error("An account with this email already exists.")

            else:

                new_user = {
                    "id": f"U{len(data['users']) + 1:03}",
                    "name": new_name,
                    "email": new_email,
                    "password": hash_password(new_password),
                    "role": "customer"
                }

                data["users"].append(new_user)
                save_data(data)

                st.success(
                    "Account created successfully. You can now sign in."
                )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

user = st.session_state.user

st.sidebar.title("🍔 ENZO")

st.sidebar.write(
    f"Welcome, **{user['name']}**"
)

st.sidebar.caption(
    f"Role: {user['role'].upper()}"
)

st.sidebar.divider()


if user["role"] == "customer":

    menu_items = [
        "🏠 Home",
        "🍔 Menu",
        "🛒 Cart",
        "📦 My Orders",
        "👤 My Account"
    ]

elif user["role"] == "staff":

    menu_items = [
        "📊 Staff Dashboard",
        "🆕 New Orders",
        "👨‍🍳 Preparing",
        "🟢 Ready Orders",
        "🔐 Pickup Verification"
    ]

else:

    menu_items = [
        "📊 Management Dashboard",
        "📦 Orders",
        "📋 Inventory",
        "🍔 Products",
        "📈 Analytics"
    ]


for item in menu_items:

    if st.sidebar.button(
        item,
        use_container_width=True
    ):

        st.session_state.page = item


st.sidebar.divider()

if st.sidebar.button(
    "🚪 Logout",
    use_container_width=True
):

    logout()


# ============================================================
# CUSTOMER HOME
# ============================================================

if user["role"] == "customer" and st.session_state.page == "🏠 Home":

    st.title("🍔 Welcome to Enzo")

    st.subheader("Order now. Come when it's ready.")

    st.write(
        "Avoid the queue. Choose your products, pay online, "
        "and visit Enzo only when your order is ready."
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Available Products",
                  len([
                      p for p in data["products"]
                      if p["available"] and p["stock"] > 0
                  ]))

    with col2:
        st.metric(
            "Your Orders",
            len(get_user_orders())
        )

    with col3:
        st.metric(
            "Items in Cart",
            sum(st.session_state.cart.values())
        )

    with col4:
        st.metric(
            "Store Status",
            "OPEN"
        )

    st.divider()

    st.success(
        "🟢 Enzo is currently accepting online orders."
    )

    if st.button(
        "🍔 Browse Menu",
        type="primary"
    ):
        st.session_state.page = "🍔 Menu"
        st.rerun()


# ============================================================
# CUSTOMER MENU
# ============================================================

elif user["role"] == "customer" and st.session_state.page == "🍔 Menu":

    st.title("🍔 Enzo Menu")

    search = st.text_input(
        "🔎 Search products"
    )

    categories = ["All"] + sorted(
        list(set(p["category"] for p in data["products"]))
    )

    category = st.selectbox(
        "Category",
        categories
    )

    products = data["products"]

    if search:
        products = [
            p for p in products
            if search.lower() in p["name"].lower()
        ]

    if category != "All":
        products = [
            p for p in products
            if p["category"] == category
        ]

    for product in products:

        col1, col2, col3 = st.columns([4, 2, 1])

        with col1:

            st.subheader(product["name"])

            st.caption(
                f"{product['category']} • "
                f"{product['stock']} left"
            )

        with col2:

            st.markdown(
                f"### ₹{product['price']}"
            )

        with col3:

            if (
                product["available"]
                and product["stock"] > 0
            ):

                if st.button(
                    "Add",
                    key=f"add_{product['id']}"
                ):

                    current = st.session_state.cart.get(
                        product["id"], 0
                    )

                    if current < product["stock"]:

                        st.session_state.cart[
                            product["id"]
                        ] = current + 1

                        st.toast(
                            f"{product['name']} added!"
                        )

                    else:
                        st.warning(
                            "Maximum available stock reached."
                        )

            else:

                st.error("OUT OF STOCK")

        st.divider()


# ============================================================
# CART
# ============================================================

elif user["role"] == "customer" and st.session_state.page == "🛒 Cart":

    st.title("🛒 Your Cart")

    if not st.session_state.cart:

        st.info("Your cart is empty.")

    else:

        total = 0

        for product_id, quantity in list(
            st.session_state.cart.items()
        ):

            product = get_product(product_id)

            if not product:
                continue

            subtotal = product["price"] * quantity
            total += subtotal

            col1, col2, col3, col4 = st.columns(
                [4, 1, 1, 1]
            )

            with col1:
                st.write(
                    f"**{product['name']}**"
                )

            with col2:
                st.write(
                    f"₹{product['price']}"
                )

            with col3:

                st.write(
                    f"Qty: {quantity}"
                )

            with col4:

                if st.button(
                    "Remove",
                    key=f"remove_{product_id}"
                ):

                    del st.session_state.cart[
                        product_id
                    ]

                    st.rerun()

        st.divider()

        st.markdown(
            f"## Total: ₹{total}"
        )

        st.write(
            "Payment will be simulated for this prototype."
        )

        payment_method = st.selectbox(
            "Payment Method",
            ["UPI", "Card", "Net Banking"]
        )

        if st.button(
            "💳 Pay & Place Order",
            type="primary",
            use_container_width=True
        ):

            # Check stock again before payment
            stock_error = False

            for product_id, quantity in st.session_state.cart.items():

                product = get_product(product_id)

                if quantity > product["stock"]:

                    st.error(
                        f"Not enough stock for {product['name']}."
                    )

                    stock_error = True

            if not stock_error:

                order_id = generate_order_id()

                items = []

                for product_id, quantity in st.session_state.cart.items():

                    product = get_product(product_id)

                    items.append({
                        "product_id": product_id,
                        "name": product["name"],
                        "price": product["price"],
                        "quantity": quantity
                    })

                    product["stock"] -= quantity

                order = {
                    "id": order_id,
                    "customer_name": user["name"],
                    "customer_email": user["email"],
                    "items": items,
                    "total": total,
                    "payment_method": payment_method,
                    "payment_status": "PAID",
                    "status": "PAYMENT VERIFIED",
                    "pickup_pin": generate_pin(),
                    "created_at": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "ready_at": None,
                    "completed_at": None
                }

                data["orders"].append(order)
                save_data(data)

                st.session_state.cart = {}

                st.success(
                    f"Order {order_id} placed successfully!"
                )

                st.session_state.page = "📦 My Orders"

                st.rerun()


# ============================================================
# CUSTOMER ORDERS
# ============================================================

elif user["role"] == "customer" and st.session_state.page == "📦 My Orders":

    st.title("📦 My Orders")

    orders = get_user_orders()

    if not orders:

        st.info("You haven't placed any orders yet.")

    else:

        for order in reversed(orders):

            st.markdown(
                f"## {order['id']}"
            )

            st.write(
                status_badge(order["status"])
            )

            st.write(
                f"Placed: {order['created_at']}"
            )

            for item in order["items"]:

                st.write(
                    f"{item['quantity']} × "
                    f"{item['name']} — "
                    f"₹{item['price'] * item['quantity']}"
                )

            st.markdown(
                f"**Total: ₹{order['total']}**"
            )

            if order["status"] == "READY":

                st.success(
                    "🎉 Your order is READY! "
                    "Please come to Enzo for pickup."
                )

                st.info(
                    f"Pickup PIN: **{order['pickup_pin']}**"
                )

                st.code(
                    f"ENZO-{order['id']}-{order['pickup_pin']}",
                    language=None
                )

            elif order["status"] == "PREPARING":

                st.warning(
                    "👨‍🍳 Your order is being prepared."
                )

            elif order["status"] == "PAYMENT VERIFIED":

                st.info(
                    "💳 Payment verified. Waiting for staff to accept the order."
                )

            elif order["status"] == "COMPLETED":

                st.success(
                    "✅ Order completed."
                )

            st.divider()


# ============================================================
# CUSTOMER ACCOUNT
# ============================================================

elif user["role"] == "customer" and st.session_state.page == "👤 My Account":

    st.title("👤 My Account")

    st.write(
        f"**Name:** {user['name']}"
    )

    st.write(
        f"**Email:** {user['email']}"
    )

    st.write(
        "**Account type:** Customer"
    )

    st.divider()

    st.subheader("Order Memory")

    st.write(
        "Your previous orders are saved automatically."
    )

    orders = get_user_orders()

    if orders:

        for order in orders[-5:]:

            st.write(
                f"{order['id']} • "
                f"₹{order['total']} • "
                f"{order['status']}"
            )


# ============================================================
# STAFF DASHBOARD
# ============================================================

elif user["role"] == "staff" and st.session_state.page == "📊 Staff Dashboard":

    st.title("📊 Staff Dashboard")

    orders = data["orders"]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "New",
            len([
                o for o in orders
                if o["status"] == "PAYMENT VERIFIED"
            ])
        )

    with col2:
        st.metric(
            "Preparing",
            len([
                o for o in orders
                if o["status"] == "PREPARING"
            ])
        )

    with col3:
        st.metric(
            "Ready",
            len([
                o for o in orders
                if o["status"] == "READY"
            ])
        )

    with col4:
        st.metric(
            "Completed",
            len([
                o for o in orders
                if o["status"] == "COMPLETED"
            ])
        )

    st.divider()

    st.info(
        "Staff workflow: "
        "PAYMENT VERIFIED → ACCEPT → PREPARING → READY → PICKUP → COMPLETED"
    )


# ============================================================
# STAFF NEW ORDERS
# ============================================================

elif user["role"] == "staff" and st.session_state.page == "🆕 New Orders":

    st.title("🆕 New Orders")

    orders = [
        o for o in data["orders"]
        if o["status"] == "PAYMENT VERIFIED"
    ]

    if not orders:

        st.success("No new orders.")

    for order in orders:

        st.subheader(
            f"{order['id']} — {order['customer_name']}"
        )

        for item in order["items"]:

            st.write(
                f"{item['quantity']} × {item['name']}"
            )

        st.write(
            f"Payment: {order['payment_status']}"
        )

        if st.button(
            "✅ Accept Order",
            key=f"accept_{order['id']}"
        ):

            order["status"] = "PREPARING"

            save_data(data)

            st.success(
                f"{order['id']} accepted."
            )

            st.rerun()

        st.divider()


# ============================================================
# STAFF PREPARING
# ============================================================

elif user["role"] == "staff" and st.session_state.page == "👨‍🍳 Preparing":

    st.title("👨‍🍳 Orders Being Prepared")

    orders = [
        o for o in data["orders"]
        if o["status"] == "PREPARING"
    ]

    if not orders:
        st.info("No orders are currently being prepared.")

    for order in orders:

        st.subheader(
            f"{order['id']} — {order['customer_name']}"
        )

        for item in order["items"]:

            st.write(
                f"{item['quantity']} × {item['name']}"
            )

        if st.button(
            "🟢 Mark READY",
            key=f"ready_{order['id']}"
        ):

            order["status"] = "READY"
            order["ready_at"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            save_data(data)

            st.success(
                f"{order['id']} is ready!"
            )

            st.rerun()

        st.divider()


# ============================================================
# STAFF READY ORDERS
# ============================================================

elif user["role"] == "staff" and st.session_state.page == "🟢 Ready Orders":

    st.title("🟢 Ready for Pickup")

    orders = [
        o for o in data["orders"]
        if o["status"] == "READY"
    ]

    if not orders:
        st.info("No ready orders.")

    for order in orders:

        st.subheader(
            f"{order['id']} — {order['customer_name']}"
        )

        st.success(
            f"Pickup PIN: {order['pickup_pin']}"
        )

        st.write(
            "Customer should provide QR/PIN before handover."
        )

        st.divider()


# ============================================================
# PICKUP VERIFICATION
# ============================================================

elif user["role"] == "staff" and st.session_state.page == "🔐 Pickup Verification":

    st.title("🔐 Pickup Verification")

    order_id = st.text_input(
        "Order ID",
        placeholder="Example: E247"
    )

    pin = st.text_input(
        "4-digit Pickup PIN"
    )

    if st.button(
        "Verify Pickup",
        type="primary"
    ):

        order = next(
            (
                o for o in data["orders"]
                if o["id"].upper() == order_id.upper()
            ),
            None
        )

        if not order:

            st.error("Order not found.")

        elif order["status"] != "READY":

            st.error(
                f"Order is currently {order['status']}."
            )

        elif order["pickup_pin"] != pin:

            st.error("Incorrect pickup PIN.")

        else:

            order["status"] = "COMPLETED"
            order["completed_at"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            save_data(data)

            st.success(
                f"✅ {order['id']} verified and completed!"
            )


# ============================================================
# MANAGEMENT DASHBOARD
# ============================================================

elif user["role"] == "admin" and st.session_state.page == "📊 Management Dashboard":

    st.title("📊 Enzo Management Dashboard")

    orders = data["orders"]

    revenue = sum(
        o["total"]
        for o in orders
        if o["payment_status"] == "PAID"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Orders",
            len(orders)
        )

    with col2:
        st.metric(
            "Revenue",
            f"₹{revenue}"
        )

    with col3:
        st.metric(
            "Active Orders",
            len([
                o for o in orders
                if o["status"] not in
                ["COMPLETED", "CANCELLED"]
            ])
        )

    with col4:
        st.metric(
            "Low Stock Items",
            len([
                p for p in data["products"]
                if p["stock"] <= p["low_stock"]
            ])
        )

    st.divider()

    st.subheader("🚨 Low Stock Alerts")

    low_stock = [
        p for p in data["products"]
        if p["stock"] <= p["low_stock"]
    ]

    if low_stock:

        for product in low_stock:

            st.warning(
                f"{product['name']}: "
                f"{product['stock']} remaining"
            )

    else:

        st.success("No low-stock products.")


# ============================================================
# MANAGEMENT ORDERS
# ============================================================

elif user["role"] == "admin" and st.session_state.page == "📦 Orders":

    st.title("📦 All Orders")

    if data["orders"]:

        rows = []

        for order in data["orders"]:

            rows.append({
                "Order": order["id"],
                "Customer": order["customer_name"],
                "Total": order["total"],
                "Payment": order["payment_status"],
                "Status": order["status"],
                "Created": order["created_at"]
            })

        df = pd.DataFrame(rows)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No orders yet.")


# ============================================================
# MANAGEMENT INVENTORY
# ============================================================

elif user["role"] == "admin" and st.session_state.page == "📋 Inventory":

    st.title("📋 Inventory Management")

    rows = []

    for product in data["products"]:

        if product["stock"] == 0:
            status = "❌ OUT OF STOCK"

        elif product["stock"] <= product["low_stock"]:
            status = "⚠️ LOW STOCK"

        else:
            status = "🟢 AVAILABLE"

        rows.append({
            "Product": product["name"],
            "Category": product["category"],
            "Stock": product["stock"],
            "Low Stock Limit": product["low_stock"],
            "Status": status
        })

    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Update Stock")

    product_names = [
        p["name"]
        for p in data["products"]
    ]

    selected_name = st.selectbox(
        "Product",
        product_names
    )

    selected_product = next(
        p for p in data["products"]
        if p["name"] == selected_name
    )

    new_stock = st.number_input(
        "New Stock Quantity",
        min_value=0,
        value=selected_product["stock"]
    )

    if st.button(
        "Update Stock",
        type="primary"
    ):

        selected_product["stock"] = new_stock

        selected_product["available"] = (
            new_stock > 0
        )

        save_data(data)

        st.success(
            f"{selected_name} stock updated."
        )

        st.rerun()


# ============================================================
# MANAGEMENT PRODUCTS
# ============================================================

elif user["role"] == "admin" and st.session_state.page == "🍔 Products":

    st.title("🍔 Product Management")

    for product in data["products"]:

        with st.expander(
            f"{product['name']} — ₹{product['price']}"
        ):

            new_price = st.number_input(
                "Price",
                min_value=0,
                value=int(product["price"]),
                key=f"price_{product['id']}"
            )

            available = st.checkbox(
                "Available for customers",
                value=product["available"],
                key=f"available_{product['id']}"
            )

            low_stock = st.number_input(
                "Low stock alert level",
                min_value=0,
                value=int(product["low_stock"]),
                key=f"low_{product['id']}"
            )

            if st.button(
                "Save Changes",
                key=f"save_{product['id']}"
            ):

                product["price"] = new_price
                product["available"] = available
                product["low_stock"] = low_stock

                save_data(data)

                st.success(
                    "Product updated."
                )

                st.rerun()


# ============================================================
# MANAGEMENT ANALYTICS
# ============================================================

elif user["role"] == "admin" and st.session_state.page == "📈 Analytics":

    st.title("📈 Enzo Analytics")

    orders = data["orders"]

    if not orders:

        st.info(
            "Analytics will appear after customers place orders."
        )

    else:

        st.subheader("Revenue")

        revenue = sum(
            o["total"]
            for o in orders
            if o["payment_status"] == "PAID"
        )

        st.metric(
            "Total Revenue",
            f"₹{revenue}"
        )

        st.subheader("Best Selling Products")

        sales = {}

        for order in orders:

            for item in order["items"]:

                name = item["name"]

                sales[name] = sales.get(
                    name, 0
                ) + item["quantity"]

        if sales:

            sales_df = pd.DataFrame(
                list(sales.items()),
                columns=["Product", "Units Sold"]
            ).sort_values(
                "Units Sold",
                ascending=False
            )

            st.bar_chart(
                sales_df.set_index("Product")
            )

        st.subheader("Order Status")

        status_counts = {}

        for order in orders:

            status = order["status"]

            status_counts[status] = (
                status_counts.get(status, 0) + 1
            )

        status_df = pd.DataFrame(
            list(status_counts.items()),
            columns=["Status", "Orders"]
        )

        st.bar_chart(
            status_df.set_index("Status")
        )


# ============================================================
# FOOTER
# ============================================================

st.sidebar.divider()

st.sidebar.caption(
    "Enzo Smart Order • Prototype"
)

st.sidebar.caption(
    "Order → Pay → Prepare → Ready → Pickup"
)
