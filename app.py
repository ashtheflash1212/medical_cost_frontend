import pickle
import numpy as np
import streamlit as st
import base64
import os

# Load the trained model
with open("random_forest_model.pkl", "rb") as file:
    model = pickle.load(file)

# Function to set a local background image and apply styling
def set_bg(image_file):
    with open(image_file, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()

    page_bg = f"""
    <style>
    .stApp {{
        color: black;
        background-image: url("data:image/jpeg;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}

    /* Title and subtitle adjustments */
    .custom-title {{
        text-align: center;
        font-weight: bold;
        padding-bottom: %;
    }}

    .custom-subtitle {{
        text-align: center;
        font-size: 18px;
        padding-top: 5%;
    }}

    /* Fix input field size */
    div[data-baseweb="select"], div[data-testid="stNumberInput"] {{
        width: 250px !important;
        font-size: 16px !important;
        margin-bottom: 12px !important;
    }}

    /* Fix label size */
    label {{
        font-size: 16px !important;
        font-weight: bold;
        color: black
    }}

    /* Fix button text size */
    .stButton > button {{
        color: white !important;
        text-align: center;
        background-color: #1E1E1E !important;
        border-radius: 8px !important;
        padding: 12px 18px !important;
        font-size: 16px !important;
        font-weight: bold !important;
    }}

    /* Center predict button */
    .button-container {{
        display: flex;
        justify-content: center;
        margin-top: 2vh;
    }}
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)

# Update the background image path
set_bg("bgaisc.jpeg") 

# Title and subtitle
st.markdown("<h1 class='custom-title'>Medical Cost Predictor</h1>", unsafe_allow_html=True)
st.markdown("<h6 class='custom-subtitle'>Enter details to predict medical costs.</h6>", unsafe_allow_html=True)

# Create columns for input fields
col1, col2 = st.columns([1, 1])

with col1:
    age = st.number_input("Age", min_value=1, max_value=120, value=30)
    bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=25.0)
    smoker = st.selectbox("Smoker", options=["yes", "no"], index=1)  # No typing allowed

with col2:
    sex = st.selectbox("Sex", options=["male", "female"], index=0)  # No typing allowed
    children = st.number_input("Number of Children", min_value=0, max_value=10, value=0)
    region = st.selectbox("Region", options=["southwest", "southeast", "northwest", "northeast"], index=0)  # No typing allowed

# Convert categorical inputs for model
sex = 1 if sex == "male" else 0
smoker = 1 if smoker == "yes" else 0
region_mapping = {"southwest": 0, "southeast": 1, "northwest": 2, "northeast": 3}
region = region_mapping[region]

# Center the predict button
st.markdown("<div class='button-container'>", unsafe_allow_html=True)
if st.button("Predict ❓"):
    input_data = np.array([[age, sex, bmi, children, smoker, region]])
    prediction = model.predict(input_data)
    st.success(f"Estimated Medical Cost 💰: ${prediction[0]:,.2f}")
st.markdown("</div>", unsafe_allow_html=True)
