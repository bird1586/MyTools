import streamlit as st
import pikepdf
import io
from pdf2image import convert_from_bytes
from PIL import Image

def unlock_pdf(pdf_file, password):
    try:
        pdf = pikepdf.open(pdf_file, password=password)
        output_buffer = io.BytesIO()
        pdf.save(output_buffer)
        pdf.close()
        return output_buffer.getvalue()
    except pikepdf._qpdf.PasswordError:
        return "Incorrect password"
    except Exception as e:
        return f"An error occurred: {e}"

def pdf_to_images(pdf_file, dpi=200):
    try:
        pdf_bytes = pdf_file.read()
        images = convert_from_bytes(pdf_bytes, dpi=dpi)
        return images
    except Exception as e:
        return f"An error occurred: {e}"

st.sidebar.title("PDF Tools")

tool = st.sidebar.selectbox("Select a tool", ["Unlock PDF", "PDF to Images"])

if tool == "Unlock PDF":
    st.title("Unlock PDF")
    uploaded_file = st.file_uploader("Upload a password-protected PDF file", type=["pdf"])
    password = st.text_input("Enter the PDF password", type="password")

    if uploaded_file and password:
        if st.button("Unlock PDF"):
            with st.spinner("Unlocking PDF..."):
                unlocked_pdf = unlock_pdf(uploaded_file, password)

            if isinstance(unlocked_pdf, bytes):
                st.success("PDF unlocked successfully!")
                st.download_button(
                    label="Download Unlocked PDF",
                    data=unlocked_pdf,
                    file_name="unlocked.pdf",
                    mime="application/pdf",
                )
            else:
                st.error(unlocked_pdf)

elif tool == "PDF to Images":
    st.title("PDF to Images")
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    dpi = st.slider("DPI (Resolution)", 100, 300, 200)

    if uploaded_file:
        if st.button("Convert to Images"):
            with st.spinner("Converting to images..."):
                images = pdf_to_images(uploaded_file, dpi=dpi)

            if isinstance(images, list):
                st.success(f"Converted {len(images)} pages to images!")
                for i, image in enumerate(images):
                    st.image(image, caption=f"Page {i+1}")
                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format='PNG')
                    st.download_button(
                        label=f"Download Page {i+1}",
                        data=img_byte_arr.getvalue(),
                        file_name=f"page_{i+1}.png",
                        mime="image/png"
                    )

            else:
                st.error(images)