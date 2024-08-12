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

# Define the calculate_total function
def calculate_total(order):
    subtotal = 0
    for item, quantity in order.items():
        subtotal += menu[item[0]][item[1]] * quantity

    total = subtotal  # No extra fees added
    return round(subtotal, 2), round(total, 2)

# Function to create a new thread and send the order to Discord
def create_thread_and_send_order(bot_token, channel_id, customer_name, phone_number, order_summary, total_price):
    # Create a new thread in the forum channel
    url = f"https://discord.com/api/v9/channels/{channel_id}/threads"
    headers = {
        "Authorization": f"Bot {bot_token}",
        "Content-Type": "application/json"
    }
    thread_data = {
        "name": f"Order from {customer_name}",
        "type": 11,  # 11 is the type for a forum post
        "auto_archive_duration": 1440  # Archive after 24 hours
    }
    response = requests.post(url, headers=headers, json=thread_data)
    
    if response.status_code == 201:
        thread_id = response.json()["id"]
        
        # Post the order details in the newly created thread
        message_url = f"https://discord.com/api/v9/channels/{thread_id}/messages"
        message_data = {
            "content": f"New Order Received:\n\nCustomer Name: {customer_name}\nPhone Number: {phone_number}\n\n{order_summary}\n**Total: ${total_price}**"
        }
        message_response = requests.post(message_url, headers=headers, json=message_data)
        
        return message_response.status_code == 200
    else:
        return False

# Streamlit Interface
st.title("🚀 Sightings Menu Calculator 🌌")

# Section for entering customer name and in-character phone number
customer_name = st.text_input("Enter your name", "")
phone_number = st.text_input("Enter your in-character phone number", "")

order = {}

# First row for menu inputs
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
    subtotal, total_price = calculate_total(order)
    order_summary = "\n".join([f"- {item} ({category}): {quantity} @ ${menu[category][item]} each"
                               for (category, item), quantity in order.items()])
    
    st.markdown(f"## Subtotal: **${subtotal}**")
    st.markdown(f"## 🧾 The total price of the order is: **${total_price}**")
    
    st.subheader("Order Summary")
    st.markdown(order_summary)

    BOT_TOKEN = st.secrets["DISCORD_BOT_TOKEN"]  # Use st.secrets for the bot token
    CHANNEL_ID = "1146423710778142780"  # Replace with your forum channel ID

    if create_thread_and_send_order(BOT_TOKEN, CHANNEL_ID, customer_name, phone_number, order_summary, total_price):
        st.success("Order sent successfully to Sightings!")
    else:
        st.error("Failed to send order to Sightings.")

