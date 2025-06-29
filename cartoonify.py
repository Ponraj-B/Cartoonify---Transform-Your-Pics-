import cv2
import numpy as np
import streamlit as st

def cartoonify_image(img):
    # Convert to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply median blur
    gray_blur = cv2.medianBlur(gray, 7)
    # Detect edges with adaptive threshold
    edges = cv2.adaptiveThreshold(
        gray_blur, 255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 9, 9
    )
    # Apply bilateral filter to reduce color palette
    color = cv2.bilateralFilter(img, d=9, sigmaColor=250, sigmaSpace=250)
    # Combine edges and color image
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon

st.title("Cartoonify Your Image")
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Original Image")

    cartoon_img = cartoonify_image(img)
    st.image(cv2.cvtColor(cartoon_img, cv2.COLOR_BGR2RGB), caption="Cartoonified Image")
