import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from io import BytesIO
import base64
import time

def image_masking_app():
    # Set the background color of the Streamlit app
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #36454F;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # File uploader
    uploaded_file = st.file_uploader("Upload an image (JPG, JPEG, PNG)...", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        # Open the uploaded image file
        original_image = Image.open(uploaded_file)
        image_bytes = BytesIO()
        original_image.save(image_bytes, format='PNG')
        image_bytes.seek(0)
        img_width, img_height = original_image.size

        # Display the original image
        st.image(original_image, caption='Original Image', use_column_width=True)

        # Masking canvas's dimensions based on the scaling factor
        default_width = 700
        scale_factor = default_width / img_width
        canvas_width = int(img_width * scale_factor)
        canvas_height = int(img_height * scale_factor)

        # Allow user to pick masking color and opacity
        mask_color = st.color_picker("Pick a mask color", "#000000")
        opacity = st.slider("Select mask opacity", 0.0, 1.0, 1.0)
        rgba_color = mask_color + hex(int(opacity * 255))[2:].zfill(2)

        # Canvas for drawing the mask
        canvas_result = st_canvas(
            fill_color=rgba_color,
            stroke_width=0,
            stroke_color="rgba(0, 0, 0, 0)",
            background_image=original_image,
            height=canvas_height,
            width=canvas_width,
            drawing_mode="rect",
            key="canvas_image",
        )

        if canvas_result.image_data is not None:
            # Convert the canvas result to a mask image
            canvas_mask = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
            if original_image.mode != 'RGBA':
                original_image = original_image.convert('RGBA')
            canvas_mask_resized = canvas_mask.resize(original_image.size)
            masked_image = Image.alpha_composite(original_image, canvas_mask_resized)

            # Display the masked image
            st.image(masked_image, caption="Masked Image", use_column_width=True)

            # Download masked image
            buffer = BytesIO()
            masked_image.save(buffer, format="PNG")
            byte_data = buffer.getvalue()

            st.download_button(
                "Download Masked Image",
                data=byte_data,
                file_name="masked_image.png",
                mime="image/png"
            )
