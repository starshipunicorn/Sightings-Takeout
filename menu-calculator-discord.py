import streamlit as st
import requests
import math

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
        "Planetary Pizza": 80.00,
        "Galaxy Guac Burger and Meteorite Fries": 122.50
    },
    "Desserts": {
        "Spacecraft S’mores Shake": 950.00,
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

# Correctly define WEBHOOK_URL and role_id outside the function
WEBHOOK_URL = st.secrets["DISCORD"]["webhook_url"]
role_id = st.secrets["DISCORD"]["role_id"]

# Function to send order to Discord with role mention outside the embed
def send_order_to_discord(customer_name, phone_number, delivery_location, area, order_summary, total_price):
    # Format the role mention with the role ID outside of the embed (in the content)
    role_mention = f"<@&{role_id}>"

    # Embed message content (without the role mention)
    embed = {
        "title": f"New Order from {customer_name}",
        "description": f"\n\n**Phone Number**: {phone_number}\n\n**Delivery Location**: {delivery_location} ({area})\n\n**Order Summary**:\n{order_summary}\n\n**Total**: ${total_price}",
        "color": 0x00ff00,  # Green color
        "fields": [
            {"name": "Customer Name", "value": customer_name, "inline": True},
            {"name": "Phone Number", "value": phone_number, "inline": True},
            {"name": "Delivery Location", "value": f"{delivery_location} ({area})", "inline": True},
            {"name": "Total", "value": f"${total_price}", "inline": False},
        ]
    }

    # The payload now contains the role mention outside the embed in 'content'
    data = {
        "content": role_mention,  # Role mention outside the embed
        "embeds": [embed]  # Embeds with order details
    }

    # Send the data to Discord via the webhook URL
    response = requests.post(WEBHOOK_URL, json=data)
    return response.status_code == 204

# Streamlit Interface
st.title("🚀 Sightings Delivery 🌌")

# Section for entering customer name, phone number, and delivery location
customer_name = st.text_input("Enter your name", "")
phone_number = st.text_input("Enter your in-character phone number", "")
delivery_location = st.text_input("Enter your exact delivery location (address or area)", "")

# Delivery location selection with "Sightings" directly included
location_type = st.radio("Select your delivery location type:", ("Sightings", "City", "Sandy", "Paleto"))

# Area selection will no longer be needed since location_type includes all options now
if location_type == "Sightings":
    area = "Sightings"
    st.write(f"You have selected **Sightings** for your delivery location (No upcharge).")
else:
    area = location_type
    st.write(f"You have selected **{area}** as your closest area for delivery.")

order = {}

# Displaying the menu and capturing orders
cols = st.columns(2)

with cols[0]:
    st.subheader("🌅 Breakfast")
    for item, price in menu["Breakfast"].items():
        quantity = st.number_input(f"{item} (${price})", min_value=0, max_value=500, step=1, key=item)
        if quantity > 0:
            order[("Breakfast", item)] = quantity

with cols[1]:
    st.subheader("🍲 Starters")
    for item, price in menu["Starters"].items():
        quantity = st.number_input(f"{item} (${price})", min_value=0, max_value=500, step=1, key=item)
        if quantity > 0:
            order[("Starters", item)] = quantity

# Second row for menu inputs
cols = st.columns(2)

with cols[0]:
    st.subheader("🍽️ Mains")
    for item, price in menu["Mains"].items():
        quantity = st.number_input(f"{item} (${price})", min_value=0, max_value=500, step=1, key=item)
        if quantity > 0:
            order[("Mains", item)] = quantity

with cols[1]:
    st.subheader("🍰 Desserts")
    for item, price in menu["Desserts"].items():
        quantity = st.number_input(f"{item} (${price})", min_value=0, max_value=500, step=1, key=item)
        if quantity > 0:
            order[("Desserts", item)] = quantity

# Third row for menu inputs
cols = st.columns(2)

with cols[0]:
    st.subheader("🍹 Alcoholic Drinks")
    for item, price in menu["Alcoholic Drinks"].items():
        quantity = st.number_input(f"{item} (${price})", min_value=0, max_value=500, step=1, key=item)
        if quantity > 0:
            order[("Alcoholic Drinks", item)] = quantity

with cols[1]:
    st.subheader("🥤 Non-Alcoholic Drinks")
    for item, price in menu["Non-Alcoholic Drinks"].items():
        quantity = st.number_input(f"{item} (${price})", min_value=0, max_value=500, step=1, key=item)
        if quantity > 0:
            order[("Non-Alcoholic Drinks", item)] = quantity

# Submit button with validation
if st.button("Submit Order"):
    if not customer_name or not phone_number or not delivery_location:
        st.warning("Please enter your name, phone number, and delivery location to submit your order.")
    else:
        # Generate the order summary and calculate the total price
        order_summary = "\n".join([f"{item} x{quantity}" for (category, item), quantity in order.items()])
        total_price = sum(menu[category][item] * quantity for (category, item), quantity in order.items())

        # Round down the total price to the nearest whole number
        total_price = math.floor(total_price)

        # Send the order to Discord
        if send_order_to_discord(customer_name, phone_number, delivery_location, area, order_summary, total_price):
            st.success(f"Order sent successfully to Sightings! A member of the team will be in contact to confirm your order. Your total is **${total_price}**.")
        else:
            st.error("Failed to send order to Sightings.")
