import streamlit as st
from pdf2image import convert_from_bytes
from PIL import Image
from io import BytesIO
import fitz  # PyMuPDF
import json
import base64

def get_base64_image(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def pdf_masking_app():
    st.subheader("Mask Information in PDFs")

    # Step 1: Upload PDF
    uploaded_pdf = st.file_uploader("Choose a PDF...", type="pdf")
    if uploaded_pdf:
        # Convert PDF pages to images
        pdf_pages = convert_from_bytes(uploaded_pdf.read(), dpi=150)

        # Step 2: Show images and allow masking
        for page_num, page_image in enumerate(pdf_pages):
            st.write(f"Page {page_num + 1}")

            # Convert image to Base64
            encoded_image = get_base64_image(page_image)

            # Display the image for masking with Fabric.js
            st.markdown(f"""
                <div id="pdf-page-{page_num}" style="position: relative; width: 700px; height: 500px;">
                    <img id="pdf-image-{page_num}" src="data:image/png;base64,{encoded_image}" 
                         style="width:100%; height:100%; z-index: 0;">
                    <canvas id="fabric-canvas-{page_num}" style="position: absolute; z-index: 1;"></canvas>
                </div>
                <button onclick="submitCoordinates()">Submit Masks</button>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/fabric.js/4.5.0/fabric.min.js"></script>
                <script>
                    var canvas{page_num} = new fabric.Canvas('fabric-canvas-{page_num}');
                    document.getElementById('pdf-image-{page_num}').onload = function() {{
                        canvas{page_num}.setHeight(500);
                        canvas{page_num}.setWidth(700);
                    }};
                    canvas{page_num}.on('mouse:down', function(e) {{
                        var pointer = canvas{page_num}.getPointer(e.e);
                        var rect = new fabric.Rect({{
                            left: pointer.x,
                            top: pointer.y,
                            width: 100,
                            height: 50,
                            fill: 'rgba(0, 0, 0, 0.5)',
                            selectable: true
                        }});
                        canvas{page_num}.add(rect);
                    }});

                    // Function to collect and send coordinates
                    function submitCoordinates() {{
                        var masks = [];
                        canvas{page_num}.getObjects().forEach(function(obj) {{
                            masks.push({{
                                left: obj.left,
                                top: obj.top,
                                width: obj.width,
                                height: obj.height
                            }});
                        }});
                        fetch('/submit_masks', {{
                            method: 'POST',
                            headers: {{
                                'Content-Type': 'application/json'
                            }},
                            body: JSON.stringify({{ page: {page_num}, masks: masks }})
                        }}).then(response => {{
                            if (response.ok) {{
                                alert('Masks submitted successfully!');
                            }} else {{
                                alert('Error submitting masks.');
                            }}
                        }});
                    }}
                </script>
            """, unsafe_allow_html=True)

        # Step 3: Initialize session state for mask_data
        if "mask_data" not in st.session_state:
            st.session_state["mask_data"] = ""

        # Text area for mask data (JSON)
        st.text_area(
            "Submitted Mask Data (JSON)",
            height=200,
            key="mask_data"
        )

        # Step 4: Apply Mask to PDF
        if st.button("Apply Mask to PDF"):
            mask_data = json.loads(st.session_state["mask_data"])
            st.write("Applying masks to the PDF...")
            masked_pdf = apply_mask_to_pdf(uploaded_pdf.read(), mask_data)

            # Provide the masked PDF as a download
            st.download_button(
                label="Download Masked PDF",
                data=masked_pdf,
                file_name="masked_output.pdf",
                mime="application/pdf"
            )


# Helper function: Apply masks and block text selectability
def apply_mask_to_pdf(uploaded_pdf, mask_data):
    """
    Apply masks to the original PDF using PyMuPDF.
    - `uploaded_pdf`: The original PDF file (uploaded by the user).
    - `mask_data`: A list of dictionaries containing mask coordinates for each page.
    """
    # Open the PDF using PyMuPDF
    pdf_document = fitz.open(stream=uploaded_pdf, filetype="pdf")

    for page_num, page_masks in enumerate(mask_data):
        page = pdf_document[page_num]  # Access the specific page

        # Apply each mask on the page
        for mask in page_masks:
            # Convert canvas coordinates to PDF coordinates
            rect = fitz.Rect(mask["left"], mask["top"], mask["left"] + mask["width"], mask["top"] + mask["height"])
            
            # Add a redaction annotation
            page.add_redact_annot(rect, fill=(0, 0, 0))  # Black mask
            
        # Apply the redaction to remove text behind the mask
        page.apply_redactions(images=True)

    # Save the redacted PDF to a BytesIO object
    output_pdf = BytesIO()
    pdf_document.save(output_pdf)
    pdf_document.close()
    output_pdf.seek(0)
    return output_pdf