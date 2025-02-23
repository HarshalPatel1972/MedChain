import streamlit as st
import requests
import random
from PIL import Image
from io import BytesIO
import cv2
import numpy as np
from pyzbar.pyzbar import decode

# ---------------------------
# Dummy ML Model Function
# ---------------------------
def predict_product_authenticity(image):
    """
    Dummy function to simulate ML prediction.
    Replace with your actual ML model inference.
    Returns a prediction (Authentic or Counterfeit) and a confidence score.
    """
    result = random.choice(["Authentic", "Counterfeit"])
    confidence = random.uniform(0.70, 0.99)
    return result, confidence

# ---------------------------
# Function to decode barcode from image using pyzbar
# ---------------------------
def decode_barcode(image: Image.Image) -> str:
    """
    Attempts to decode a barcode from the provided PIL image.
    Returns the barcode data as string if found, otherwise None.
    """
    # Convert PIL image to OpenCV format
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    decoded_objects = decode(image_cv)
    if decoded_objects:
        # Return first decoded barcode data (as string)
        return decoded_objects[0].data.decode("utf-8")
    else:
        return None

# ---------------------------
# Function to Verify Barcode via Verbwire API
# ---------------------------
def verify_barcode_with_verbwire(barcode):
    """
    Calls the Verbwire API to verify a barcode on the Polygon blockchain.
    Update URL and payload according to your Verbwire setup.
    """
    api_key = st.secrets.get("VERBWIRE_API_KEY", "your_verbwire_api_key_here")
    
    url = "https://api.verbwire.com/v1/your_blockchain_endpoint"  # Placeholder URL
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "barcode": barcode,
        "chain": "polygon"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            product_info = response.json().get("product_info", {})
            return product_info
        else:
            st.error("Error from Verbwire API: " + response.text)
            return None
    except Exception as e:
        st.error("Error contacting Verbwire API: " + str(e))
        return None

# ---------------------------
# Streamlit App UI
# ---------------------------
st.set_page_config(page_title="MedChain Authenticator", layout="wide")
st.title("MedChain Authenticator")
st.markdown("### Verify Product Authenticity Using AI & Blockchain on Polygon")
st.write("Scan a product or its barcode to determine if it's authentic, and view product details from the blockchain.")

# Create two tabs: one for image-based product verification and one for barcode verification.
tab1, tab2 = st.tabs(["Product Image Verification", "Barcode Verification"])

# ---------------------------
# Tab 1: Product Image Verification
# ---------------------------
with tab1:
    st.header("Product Verification via Image Scan")
    st.markdown("Upload an image of the product packaging to assess its authenticity.")
    uploaded_image = st.file_uploader("Choose a product image", type=["jpg", "jpeg", "png"])
    
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
# Tab 2: Barcode Verification via Blockchain
# ---------------------------
with tab2:
    st.header("Barcode Verification via Blockchain")
    st.markdown("You can either manually enter the barcode number or scan a barcode image.")
    
    # Provide a radio option to choose the method
    method = st.radio("Select Barcode Input Method", ("Enter Manually", "Scan Barcode Image"))
    
    barcode_value = None
    if method == "Enter Manually":
        barcode_value = st.text_input("Enter the product barcode or QR code number")
    else:
        st.markdown("Upload an image containing the barcode:")
        barcode_image_file = st.file_uploader("Barcode Image", type=["jpg", "jpeg", "png"], key="barcode")
        if barcode_image_file is not None:
            barcode_image = Image.open(barcode_image_file)
            st.image(barcode_image, caption="Uploaded Barcode Image", use_column_width=True)
            barcode_value = decode_barcode(barcode_image)
            if barcode_value:
                st.success(f"Decoded Barcode: **{barcode_value}**")
            else:
                st.error("No barcode could be decoded from the image. Please try another image.")
    
    if st.button("Verify Barcode"):
        if barcode_value:
            st.info("Verifying barcode on Polygon via Verbwire API...")
            product_info = verify_barcode_with_verbwire(barcode_value)
            if product_info:
                st.subheader("Product Information from Blockchain:")
                for key, value in product_info.items():
                    st.markdown(f"**{key}:** {value}")
            else:
                st.error("No product information found or an error occurred during verification.")
        else:
            st.error("Please provide a valid barcode value either manually or by scanning an image.")
