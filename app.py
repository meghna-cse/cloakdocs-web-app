import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from io import BytesIO

# Streamlit app title
st.title("Document & Image Masking Web Application")

# File uploader
uploaded_file = st.file_uploader("Choose an image (JPG, JPEG, PNG)...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Open the uploaded image file
    original_image = Image.open(uploaded_file)

    # Display the original image
    st.image(original_image, caption='Original Image', use_column_width=True)

    # Convert the image to RGBA if it isn't already (to allow transparency)
    if original_image.mode != 'RGBA':
        original_image = original_image.convert('RGBA')

    # Get the image dimensions
    img_width, img_height = original_image.size

    # Allow user to pick masking color and opacity
    mask_color = st.color_picker("Pick a mask color", "#000000")  # Default black mask
    opacity = st.slider("Select mask opacity", 0.0, 1.0, 0.3)  # Default opacity is 30%
    rgba_color = mask_color + hex(int(opacity * 255))[2:].zfill(2)

    # Write instructions for the user
    st.write("Draw on the image to apply masking. The canvas size is dynamically set based on the uploaded image size:")

    # Create a canvas that uses the original image dimensions with no scaling or resizing
    canvas_result = st_canvas(
        fill_color=rgba_color,  # Mask color with opacity
        stroke_width=0,  # No outline/stroke
        stroke_color="rgba(0, 0, 0, 0)",  # Transparent stroke color
        background_image=original_image,  # Use the original image as the canvas background
        height=img_height,  # Set canvas height to match the image height
        width=img_width,  # Set canvas width to match the image width
        drawing_mode="rect",  # Drawing rectangles for masking
        key="canvas",
    )

    # Check if any masking was applied
    if canvas_result.image_data is not None:
        # Convert the canvas result to a mask image
        canvas_mask = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')

        # Composite the canvas mask over the original image
        masked_image = Image.alpha_composite(original_image, canvas_mask)

        # Display the final masked image in the app
        st.image(masked_image, caption="Masked Image", use_column_width=True)

        # Provide download button for masked image
        buffer = BytesIO()
        masked_image.save(buffer, format="PNG")
        byte_data = buffer.getvalue()

        st.download_button(
            "Download Masked Image",
            data=byte_data,
            file_name="masked_image.png",
            mime="image/png"
        )
