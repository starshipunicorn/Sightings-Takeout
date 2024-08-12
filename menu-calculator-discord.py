import streamlit as st
import requests

# Define the menu dictionary
menu = {
    "Breakfast": {
        "Crater Cinnamon Roll Pancakes": 73.50,
        "Nebula Nosh Chicken & Waffles": 115.50,
        "Extraterrestrial Omelet": 87.50
    },
    "Starters": {
        "Celestial Caesar Salad": 70.00,
        "Alien Antenna Bites": 98.00,
        "Orbiting Onion Rings": 52.50
    },
    "Mains": {
        "Celestial Creature Gyro": 115.50,
        "Andromeda Invader Curry": 105.00,
        "Planetary Pizza": 70.00,
        "Galaxy Guac Burger and Meteorite Fries": 122.50
    },
    "Desserts": {
        "Spacecraft S’mores Shake": 56.00,
        "Blackhole Brownies": 66.50,
        "Martian Mousse": 73.50
    },
    "Alcoholic Drinks": {
        "UFO Umbrella Drink": 50.00,
        "Asteroid Amaretto Sour": 57.50,
        "Alien Ambrosia": 62.50
    },
    "Non-Alcoholic Drinks": {
        "Lunar Lemonade": 27.50,
        "Comet Cola Float": 32.50,
        "Galactic Grape Cola": 27.50,
        "Nebula Nectar Cola": 27.50
    }
}

# Webhook URL (replace with your actual webhook URL)
WEBHOOK_URL = "https://discord.com/api/webhooks/1272653289984364654/GiWp1B37ITq2yvtLWRfIGY7IIIzOIAyI4s2LXDYbjv_aJMc-q8jFZrowYGScKeC4Tuz7"

# Function to send order to Discord using a webhook with an embed
def send_order_to_discord(customer_name, phone_number, order_summary, total_price):
    embed = {
        "title": f"New Order from {customer_name}",
        "description": f"**Phone Number**: {phone_number}\n\n**Order Summary**:\n{order_summary}\n\n**Total**: ${total_price}",
        "color": 0x00ff00,  # Green color, you can change it to another color
        "fields": [
            {"name": "Customer Name", "value": customer_name, "inline": True},
            {"name": "Phone Number", "value": phone_number, "inline": True},
            {"name": "Total", "value": f"${total_price}", "inline": False},
        ]
    }

    data = {
        "embeds": [embed]  # Embeds must be passed as an array
    }

    response = requests.post(WEBHOOK_URL, json=data)
    return response.status_code == 204

# Streamlit Interface
st.title("🚀 Sightings Menu Calculator 🌌")

# Section for entering customer name and in-character phone number
customer_name = st.text_input("Enter your name", "")
phone_number = st.text_input("Enter your in-character phone number", "")

order = {}

# Displaying the menu and capturing orders
cols = st.columns(2)

with cols[0]:
    st.subheader("🌅 Breakfast")
    for item, price in menu["Breakfast"].items():
        quantity = st.number_input(f"{item} (${price})", min_value=0, max_value=10, step=1, key=item)
        if quantity > 0:
            order[("Breakfast", item)] = quantity

with cols[1]:
    st.subheader("🍲 Starters")
    for item, price in menu["Starters"].items():
        quantity = st.number_input(f"{item} (${price})", min_value=0, max_value=10, step=1, key=item)
        if quantity > 0:
            order[("Starters", item)] = quantity

# Second row for menu inputs
cols = st.columns(2)

with cols[0]:
    st.subheader("🍽️ Mains")
    for item, price in menu["Mains"].items():
        quantity = st.number_input(f"{item} (${price})", min_value=0, max_value=10, step=1, key=item)
        if quantity > 0:
            order[("Mains", item)] = quantity

with cols[1]:
    st.subheader("🍰 Desserts")
    for item, price in menu["Desserts"].items():
        quantity = st.number_input(f"{item} (${price})", min_value=0, max_value=10, step=1, key=item)
        if quantity > 0:
            order[("Desserts", item)] = quantity

# Third row for menu inputs
cols = st.columns(2)

with cols[0]:
    st.subheader("🍹 Alcoholic Drinks")
    for item, price in menu["Alcoholic Drinks"].items():
        quantity = st.number_input(f"{item} (${price})", min_value=0, max_value=10, step=1, key=item)
        if quantity > 0:
            order[("Alcoholic Drinks", item)] = quantity

with cols[1]:
    st.subheader("🥤 Non-Alcoholic Drinks")
    for item, price in menu["Non-Alcoholic Drinks"].items():
        quantity = st.number_input(f"{item} (${price})", min_value=0, max_value=10, step=1, key=item)
        if quantity > 0:
            order[("Non-Alcoholic Drinks", item)] = quantity

if st.button("Submit Order"):
    # Generate the order summary and calculate the total price
    order_summary = "\n".join([f"{item} x{quantity}" for (category, item), quantity in order.items()])
    total_price = sum(menu[category][item] * quantity for (category, item), quantity in order.items())

    if send_order_to_discord(customer_name, phone_number, order_summary, total_price):
        st.success("Order sent successfully to Sightings!")
    else:
        st.error("Failed to send order to Sightings.")
