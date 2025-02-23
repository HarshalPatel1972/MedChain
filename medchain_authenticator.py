import streamlit as st
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
    Replace with your actual ML model inference later.
    Returns a prediction (Authentic or Counterfeit) and a confidence score.
    """
    result = random.choice(["Authentic", "Counterfeit"])
    confidence = random.uniform(0.70, 0.99)
    return result, confidence

# ---------------------------
# Function to decode barcode from image
# ---------------------------
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
# Dummy function for blockchain barcode verification
# ---------------------------
def verify_barcode_on_polygon(barcode):
    """
    Dummy function for blockchain integration.
    Replace with actual blockchain call when ready.
    """
    return {
        "status": "Not Implemented",
        "message": "Blockchain integration coming soon.",
        "barcode": barcode
    }

# ---------------------------
# Streamlit App UI
# ---------------------------
st.set_page_config(page_title="MedChain Authenticator", layout="wide")
st.title("MedChain Authenticator")
st.markdown("### Verify Product Authenticity Using AI (Blockchain integration coming soon)")
st.write("Scan a product image or its barcode to determine if it's authentic.")

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
    st.markdown("You can either manually enter the barcode or scan a barcode image.")
    
    method = st.radio("Select Barcode Input Method", ("Enter Manually", "Scan Barcode Image"))
    
    barcode_value = None
    if method == "Enter Manually":
        barcode_value = st.text_input("Enter product barcode")
    else:
        barcode_image_file = st.file_uploader("Upload barcode image", type=["jpg", "jpeg", "png"], key="barcode")
        if barcode_image_file is not None:
            barcode_image = Image.open(barcode_image_file)
            st.image(barcode_image, caption="Uploaded Barcode Image", use_column_width=True)
            barcode_value = decode_barcode(barcode_image)
            if barcode_value:
                st.success(f"Decoded Barcode: **{barcode_value}**")
            else:
                st.error("Could not decode barcode.")
    
    if st.button("Verify Barcode"):
        if barcode_value:
            st.info("Verifying barcode... (Blockchain integration coming soon)")
            product_info = verify_barcode_on_polygon(barcode_value)
            st.subheader("Product Information (Dummy Data):")
            st.json(product_info)
        else:
            st.error("Please enter or scan a valid barcode.")
