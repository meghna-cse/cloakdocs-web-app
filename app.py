import streamlit as st
from image_masking import image_masking_app
from pdf_masking import pdf_masking_app

# Streamlit app title
st.title("CloakDocs")

# Links to GitHub and LinkedIn
st.markdown(
    """
    <div style="display: flex; align-items: center;">
        <a href="https://github.com/meghna-cse/cloakdocs-web-app" target="_blank">
            <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" width="20" height="20" style="margin-right: 10px;">
        </a>
    </div>
    """, unsafe_allow_html=True
)
st.sidebar.title("Select Functionality")

# Sidebar for navigation
option = st.sidebar.radio("What would you like to do?", ("Image Masking", "PDF Masking"))

# Route to the appropriate module
if option == "Image Masking":
    image_masking_app()
elif option == "PDF Masking":
    pdf_masking_app()
