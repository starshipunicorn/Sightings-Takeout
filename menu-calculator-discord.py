import streamlit as st
import requests
import math

# 🚀 Menu
menu = {
    "Breakfast": {
        "Supernova Breakfast Sandwich": 110,
        "Crater Cinnamon Roll Pancakes": 75,
        "Nebula Nosh Chicken & Waffles": 120
    },
    "Main Dishes": {
        "Galaxy Guac Burger": 125,
        "Cosmic Corndog": 85,
        "Andromeda Invader Curry": 105,
        "Protostar Pulled Pork Sandwich": 125,
        "Planetary Pizza": 95,
        "Big Dipper Birria Tacos": 95
    },
    "Desserts": {
        "Martian Mousse": 75,
        "Black Hole Brownies": 70,
        "Pie in the Sky": 75,
        "Astronaut Ice Cream": 75,
        "Chocolate Milky Way": 75,
        "Spacecraft S’mores Shake": 450
    },
    "Beverages": {
        "Starlight Lemonade": 28,
        "Lunar Lemonade": 27,
        "Galactic Grape Soda": 27,
        "Nebula Nectar Cola": 27,
        "Horchata": 30,
        "Comet Cola Float": 52
    },
    "Extras": {
        "Preservatives": 30
    }
}

WEBHOOK_URL = st.secrets["DISCORD"]["webhook_url"]
role_id = st.secrets["DISCORD"]["role_id"]

def send_order_to_discord(customer_name, phone_number, delivery_location, area, order_summary, total_price):
    role_mention = f"<@&{role_id}>"
    embed = {
        "title": f"New Order from {customer_name}",
        "description": f"\n\n**Phone Number**: {phone_number}\n\n**Delivery Location**: {delivery_location} ({area})\n\n**Order Summary**:\n{order_summary}\n\n**Total**: ${total_price}",
        "color": 0x00ff00,
        "fields": [
            {"name": "Customer Name", "value": customer_name, "inline": True},
            {"name": "Phone Number", "value": phone_number, "inline": True},
            {"name": "Delivery Location", "value": f"{delivery_location} ({area})", "inline": True},
            {"name": "Total", "value": f"${total_price}", "inline": False},
        ]
    }
    data = {"content": role_mention, "embeds": [embed]}
    response = requests.post(WEBHOOK_URL, json=data)
    return response.status_code == 204

# 🎨 App UI
st.set_page_config(page_title="Sightings Delivery", layout="centered")
st.title("🚀 Sightings Delivery 🌌")
st.markdown("_ExtraTerrestrial Flavors & Comfort Bites_")

# 📝 Customer Info
customer_name = st.text_input("Enter your name", "")
phone_number = st.text_input("Enter your in-character phone number", "")
delivery_location = st.text_input("Enter your exact delivery location (address or area)", "")
location_type = st.radio("Select your delivery location type:", ("Sightings", "City", "Sandy", "Paleto"))

area = location_type
if area == "Sightings":
    st.write("You have selected **Sightings** for your delivery location (No upcharge).")
else:
    st.write(f"You have selected **{area}** as your closest area for delivery.")

# 🛒 Order Inputs
order = {}
for section, items in menu.items():
    with st.expander(f"🛸 {section}", expanded=True):
        for item, price in items.items():
            qty = st.number_input(f"{item} (${price})", min_value=0, max_value=500, step=1, key=f"{section}_{item}")
            if qty > 0:
                order[(section, item)] = qty

# 🧠 State control for calculate/submit
if "calculated" not in st.session_state:
    st.session_state.calculated = False
if "total_price" not in st.session_state:
    st.session_state.total_price = 0
if "order_summary" not in st.session_state:
    st.session_state.order_summary = ""

# 🔢 Calculate total
if st.button("Calculate Total"):
    if not order:
        st.warning("Please select at least one item to calculate your total.")
    else:
        base_total = sum(menu[category][item] * qty for (category, item), qty in order.items())
        total_price = math.floor(base_total)
        order_summary = "\n".join([f"{item} x{qty}" for (_, item), qty in order.items()])

        st.session_state.total_price = total_price
        st.session_state.order_summary = order_summary
        st.session_state.calculated = True

# 🧾 If calculated, show summary + submit option
if st.session_state.calculated:
    st.markdown("---")
    st.markdown(f"### 🌌 Subtotal: **${st.session_state.total_price}**")
    st.subheader("📦 Order Summary")
    for (cat, item), qty in order.items():
        st.markdown(f"- **{item}** ({cat}) × {qty} @ ${menu[cat][item]} each")

    # ✅ Submission readiness
    ready_to_submit = st.checkbox("✅ I’m ready to submit this order")

    if ready_to_submit:
        if st.button("Submit Order"):
            if not customer_name or not phone_number or not delivery_location:
                st.warning("Please enter your name, phone number, and delivery location to submit your order.")
            else:
                success = send_order_to_discord(
                    customer_name,
                    phone_number,
                    delivery_location,
                    area,
                    st.session_state.order_summary,
                    st.session_state.total_price
                )
                if success:
                    st.success(f"Order sent successfully to Sightings! Your total is **${st.session_state.total_price}**. A team member will be in contact soon.")
                    st.session_state.calculated = False
                else:
                    st.error("Failed to send order to Sightings.")
