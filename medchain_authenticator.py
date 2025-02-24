import streamlit as st
import random
import json
import os
from PIL import Image
from io import BytesIO
import cv2
import numpy as np
from pyzbar.pyzbar import decode

# ---------------------------
# Configuration
# ---------------------------
# Use a relative path so that it works on Streamlit Cloud if the file is in the same repo.
MAPPING_FILE = "./barcode_mapping.json"

# ---------------------------
# Helper Functions
# ---------------------------

def load_mapping():
    """
    Loads the barcode mapping JSON file (which contains GTIN -> product details).
    Returns a dictionary if found, else an empty dict.
    """
    if not os.path.exists(MAPPING_FILE):
        st.error(f"Mapping file not found: {MAPPING_FILE}")
        return {}
    try:
        with open(MAPPING_FILE, "r") as f:
            mapping_data = json.load(f)
        return mapping_data
    except Exception as e:
        st.error(f"Error loading mapping file: {e}")
        return {}

def lookup_gtin(gtin_input, mapping):
    """
    Given a GTIN input (barcode number) and the mapping dict,
    returns a dict of product details if found, else None.
    The mapping is assumed to be keyed by product name,
    with a 'gtin' field inside each product's details.
    """
    for product_name, details in mapping.items():
        if details.get("gtin") == gtin_input:
            return details
    return None

def predict_product_authenticity(image):
    """
    Dummy function to simulate ML prediction for product authenticity.
    Replace with your actual ML model inference later.
    Returns a prediction (Authentic or Counterfeit) and a confidence score.
    """
    result = random.choice(["Authentic", "Counterfeit"])
    confidence = random.uniform(0.70, 0.99)
    return result, confidence

def decode_barcode(image: Image.Image) -> str:
    """
    Attempts to decode a barcode from the provided PIL image.
    Returns the barcode data as string if found, otherwise None.
    """
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    decoded_objects = decode(image_cv)
    if decoded_objects:
        return decoded_objects[0].data.decode("utf-8")
    return None

# ---------------------------
# Streamlit App UI
# ---------------------------
st.set_page_config(page_title="MedChain Authenticator", layout="wide")
st.title("MedChain Authenticator")
st.markdown("### Verify Product Authenticity Using AI + Barcode Lookup")
st.write("Scan a product image or its barcode to determine if it's authentic, and retrieve product details.")

# Create two tabs: one for product image verification and one for barcode verification.
product_tab, barcode_tab = st.tabs(["Product Image Verification", "Barcode Verification"])

# ---------------------------
# Tab 1: Product Image Verification
# ---------------------------
with product_tab:
    st.header("Product Verification via Image Scan")
    uploaded_image = st.file_uploader("Upload product image", type=["jpg", "jpeg", "png"])
    
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Product Image", use_column_width=True)
        
        if st.button("Verify Product Authenticity"):
            result, confidence = predict_product_authenticity(image)
            st.markdown(f"**Prediction:** {result}")
            st.markdown(f"**Confidence:** {confidence:.2f}")
            if result == "Authentic":
                st.success("This product appears to be authentic.")
            else:
                st.error("This product appears to be counterfeit.")

# ---------------------------
# Tab 2: Barcode Verification
# ---------------------------
with barcode_tab:
    st.header("Barcode Verification")
    st.markdown("You can either manually enter the barcode (GTIN) or scan a barcode image.")
    
    # Radio buttons to choose input method
    method = st.radio("Select Barcode Input Method", ("Enter Manually", "Scan Barcode Image"))
    
    barcode_value = None
    if method == "Enter Manually":
        barcode_value = st.text_input("Enter product barcode (GTIN)")
    else:
        barcode_image_file = st.file_uploader("Upload barcode image", type=["jpg", "jpeg", "png"], key="barcode")
        if barcode_image_file is not None:
            barcode_image = Image.open(barcode_image_file)
            st.image(barcode_image, caption="Uploaded Barcode Image", use_column_width=True)
            decoded_value = decode_barcode(barcode_image)
            if decoded_value:
                barcode_value = decoded_value
                st.success(f"Decoded Barcode: **{barcode_value}**")
            else:
                st.error("Could not decode barcode.")
    
    # Button to verify the barcode
    if st.button("Verify Barcode"):
        if barcode_value:
            # Load the mapping from the JSON file
            mapping_data = load_mapping()
            if not mapping_data:
                st.error("Mapping data is empty or could not be loaded.")
            else:
                # Lookup the GTIN in the mapping
                product_info = lookup_gtin(barcode_value, mapping_data)
                if product_info:
                    st.subheader("Product Details:")
                    st.markdown(f"**Product Name:** {product_info.get('product_name', 'N/A')}")
                    st.markdown(f"**Manufacturer:** {product_info.get('manufacturer', 'N/A')}")
                    st.markdown(f"**GTIN:** {product_info.get('gtin', 'N/A')}")
                    st.markdown(f"**Manufacturing Date:** {product_info.get('mfg_date', 'N/A')}")
                    st.markdown(f"**Expiry Date:** {product_info.get('expiry_date', 'N/A')}")
                else:
                    st.error("Barcode (GTIN) not found in mapping.")
        else:
            st.error("Please enter or scan a valid barcode.")
