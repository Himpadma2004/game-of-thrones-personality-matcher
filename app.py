import streamlit as st
import pickle
import requests
import numpy as np
import pandas as pd

# --- Load or create data.pkl ---
# This should be done separately in a notebook/script. 
# If data.pkl already exists, just load it:
df = pickle.load(open('data.pkl','rb'))

# Fetch Game of Thrones API data for images
api_data = requests.get("https://thronesapi.com/api/v2/Characters").json()

# Optional: fix character names for display
df['character'] = df['character'].replace({
    'Jaime': 'Jamie',
    'Lord Varys': 'Varys',
    'Bronn': 'Lord Bronn',
    'Sandor Clegane': 'The Hound',
    'Robb Stark': 'Rob Stark'
})

# --- Function to fetch image ---
def fetch_image(name, api_data):
    for item in api_data:
        if item['fullName'] == name:
            return item['imageUrl']
    return None

# --- Streamlit UI ---
st.title("Game Of Thrones Personality Matcher")

# Character dropdown (all characters)
selected_character = st.selectbox("Select a character", df['character'].values)

# --- Compute closest personality match ---
character_id = np.where(df['character'].values == selected_character)[0][0]
coords = df[['x','y']].values

# Euclidean distances
distances = [np.linalg.norm(coords[character_id] - coords[i]) for i in range(len(coords))]

# Closest match (skip self)
recommended_id = sorted(list(enumerate(distances)), key=lambda x: x[1])[1][0]
recommended_character = df['character'].values[recommended_id]

# Fetch images
selected_image = fetch_image(selected_character, api_data)
recommended_image = fetch_image(recommended_character, api_data)

# --- Display results in two columns ---
col1, col2 = st.columns(2)

with col1:
    st.header(selected_character)
    if selected_image:
        st.image(selected_image)
    else:
        st.text("Image not found")

with col2:
    st.header(recommended_character)
    if recommended_image:
        st.image(recommended_image)
    else:
        st.text("Image not found")
