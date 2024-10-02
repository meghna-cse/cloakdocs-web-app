import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from io import BytesIO
import base64

# Function to encode the image to Base64
def encode_image(image: Image.Image) -> str:
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# Function to decode the Base64 image back to a PIL Image
def decode_image(encoded_image: str) -> Image.Image:
    img_bytes = base64.b64decode(encoded_image.encode())
    image = Image.open(BytesIO(img_bytes))
    return image

# Function to convert the PIL image to an in-memory BytesIO object
def get_image_bytes(image: Image.Image) -> BytesIO:
    img_bytes = BytesIO()
    image.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

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

# Streamlit app title
st.title("CloakDocs")
st.subheader("A Web App for Masking Information in Images")

# Links to GitHub and LinkedIn
st.markdown(
    """
    <div style="display: flex; align-items: center;">
        <a href="https://github.com/meghna-cse/cloakdocs-web-app" target="_blank">
            <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" width="20" height="20" style="margin-right: 10px;">
        </a>
        <a href="https://linkedin.com/in/meghna-j" target="_blank">
            <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" width="20" height="20">
        </a>
    </div>
    """, unsafe_allow_html=True
)

# File uploader
uploaded_file = st.file_uploader("Choose an image (JPG, JPEG, PNG)...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Open the uploaded image file
    original_image = Image.open(uploaded_file)
    image_bytes = get_image_bytes(original_image)  # Get the image as bytes to avoid external file paths
    img_width, img_height = original_image.size

    # Display the original image
    st.image(image_bytes, caption='Original Image', use_column_width=True) 

    # Get the widths for the masking canvas
    original_image_for_canvas = Image.open(image_bytes)  # Convert the image bytes to PIL Image for background use in the canvas
    default_width = 700
    scale_factor = default_width / img_width

    # Masking canvas's dimensions based on the scaling factor
    canvas_width = int(img_width * scale_factor)
    canvas_height = int(img_height * scale_factor)

    # Allow user to pick masking color and opacity
    mask_color = st.color_picker("Pick a mask color", "#000000")  # Default black mask
    opacity = st.slider("Select mask opacity", 0.0, 1.0, 1.0)  # Default opacity is 100%
    rgba_color = mask_color + hex(int(opacity * 255))[2:].zfill(2)

    st.write("Draw on the image to apply masking. The canvas size is dynamically set based on the uploaded image size:")

    # Encode and then decode the image for the canvas
    encoded_image = encode_image(original_image_for_canvas)
    decoded_image = decode_image(encoded_image)

    canvas_result = st_canvas(
        fill_color=rgba_color,  # Mask color with opacity
        stroke_width=0,  # No outline/stroke
        stroke_color="rgba(0, 0, 0, 0)",  # Transparent stroke color
        background_image=decoded_image,  # Using the decoded image object
        height=canvas_height,
        width=canvas_width,
        drawing_mode="rect",  # Drawing rectangles for masking
        key="canvas",
    )

    # Check if any masking was applied
    if canvas_result.image_data is not None:
        # Convert the canvas result to a mask image
        canvas_mask = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')

        # Composite the canvas mask over the original image
        if original_image.mode != 'RGBA':
            original_image = original_image.convert('RGBA')
        canvas_mask_resized = canvas_mask.resize(original_image.size)
        masked_image = Image.alpha_composite(original_image, canvas_mask_resized)

        # Display the final masked image in the app
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

st.write("🚀 Working on new feature: PDF support coming soon!")