import streamlit as st
import requests
import math

# 🚀 Updated menu with Extras
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

# 🌐 Discord webhook details
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

# 🎨 App layout
st.set_page_config(page_title="Sightings Delivery", layout="centered")
st.title("🚀 Sightings Delivery 🌌")
st.markdown("_ExtraTerrestrial Flavors & Comfort Bites_")

# 📝 Customer info
customer_name = st.text_input("Enter your name", "")
phone_number = st.text_input("Enter your in-character phone number", "")
delivery_location = st.text_input("Enter your exact delivery location (address or area)", "")
location_type = st.radio("Select your delivery location type:", ("Sightings", "City", "Sandy", "Paleto"))

area = location_type
if area == "Sightings":
    st.write("You have selected **Sightings** for your delivery location (No upcharge).")
else:
    st.write(f"You have selected **{area}** as your closest area for delivery.")

# 🛒 Order form
order = {}
for section, items in menu.items():
    with st.expander(f"🛸 {section}", expanded=True):
        for item, price in items.items():
            qty = st.number_input(f"{item} (${price})", min_value=0, max_value=500, step=1, key=f"{section}_{item}")
            if qty > 0:
                order[(section, item)] = qty

# ✅ Submit order
if st.button("Submit Order"):
    if not customer_name or not phone_number or not delivery_location:
        st.warning("Please enter your name, phone number, and delivery location to submit your order.")
    else:
        # 🧾 Create summary
        order_summary = "\n".join([f"{item} x{qty}" for (_, item), qty in order.items()])
        base_total = sum(menu[category][item] * qty for (category, item), qty in order.items())
        total_price = math.floor(base_total)

        if send_order_to_discord(customer_name, phone_number, delivery_location, area, order_summary, total_price):
            st.success(f"Order sent successfully to Sightings! Your total is **${total_price}**. A team member will be in contact soon.")
        else:
            st.error("Failed to send order to Sightings.")
