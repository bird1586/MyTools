import streamlit as st
import pikepdf
import io
import fitz  # PyMuPDF

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
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        images = []
        for page in doc:
            pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))  # Convert to pixels
            img_bytes = pix.tobytes("png")  # Convert to PNG bytes
            images.append(img_bytes)
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
    dpi = st.selectbox("Select DPI (Resolution)", [100, 200, 300]) #changed to selectbox

    if uploaded_file:
        if st.button("Convert to Images"):
            with st.spinner("Converting to images..."):
                images = pdf_to_images(uploaded_file, dpi=dpi)

            if isinstance(images, list):
                st.success(f"Converted {len(images)} pages to images!")
                for i, img_bytes in enumerate(images):
                    st.image(img_bytes, caption=f"Page {i+1}")
                    st.download_button(
                        label=f"Download Page {i+1}",
                        data=img_bytes,
                        file_name=f"page_{i+1}.png",
                        mime="image/png"
                    )
            else:
                st.error(images)
