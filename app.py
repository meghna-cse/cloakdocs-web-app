import streamlit as st
from PIL import Image, ImageEnhance
import fitz  # PyMuPDF

st.title("Document & Image Masking Web Application")

# File uploader (for both images and PDFs)
uploaded_file = st.file_uploader("Choose a file (JPG, JPEG, PNG, PDF)...", type=["jpg", "jpeg", "png", "pdf"])

# Handling image uploads
if uploaded_file and uploaded_file.type in ["image/jpeg", "image/png"]:
    # Open and display the image
    image = Image.open(uploaded_file)
    st.image(image, caption='Original Image', use_column_width=True)

    # Add a slider to control masking opacity
    opacity = st.slider("Select masking opacity (0 for no mask, 1 for full mask)", 0.0, 1.0, 0.5)

    # Apply a masking layer (using opacity)
    enhancer = ImageEnhance.Brightness(image)
    masked_image = enhancer.enhance(1 - opacity)

    # Display and download the masked image
    st.image(masked_image, caption='Masked Image', use_column_width=True)
    st.download_button("Download Masked Image", masked_image.tobytes(), file_name="masked_image.png", mime="image/png")

# Handling PDF uploads
elif uploaded_file and uploaded_file.type == "application/pdf":
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    page = doc.load_page(0)  # Load the first page
    pix = page.get_pixmap()  # Render the page to an image

    # Convert pixmap to an image using PIL
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Display the original PDF page as an image
    st.image(image, caption='Original PDF Page', use_column_width=True)

    # Add a slider to control masking opacity
    opacity = st.slider("Select masking opacity (0 for no mask, 1 for full mask)", 0.0, 1.0, 0.5)

    # Apply a masking layer (using opacity)
    enhancer = ImageEnhance.Brightness(image)
    masked_image = enhancer.enhance(1 - opacity)

    # Display and download the masked PDF page as an image
    st.image(masked_image, caption='Masked PDF Page', use_column_width=True)
    st.download_button("Download Masked PDF Page", masked_image.tobytes(), file_name="masked_pdf_page.png", mime="image/png")
