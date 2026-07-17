import streamlit as st
import fitz
from io import BytesIO

from utils import image_to_pdf
from utils import docx_to_pdf
from utils import merge_pdfs


st.set_page_config(
    page_title="Smart PDF Merger",
    layout="wide"
)

st.title("📄 Smart PDF Merger")

uploaded_files = st.file_uploader(
    "Upload PDF / DOCX / Images",
    type=["pdf","docx","png","jpg","jpeg"],
    accept_multiple_files=True
)


if uploaded_files:

    pdf_list=[]

    for file in uploaded_files:

        ext=file.name.split(".")[-1].lower()

        if ext=="pdf":
            pdf_list.append(file)

        elif ext=="docx":
            pdf_list.append(docx_to_pdf(file))

        else:
            pdf_list.append(image_to_pdf(file))

    if st.button("Merge Files"):

        merged_pdf=merge_pdfs(pdf_list)

        st.success("Merged Successfully")

        st.download_button(
            "Download PDF",
            merged_pdf,
            file_name="Merged.pdf",
            mime="application/pdf"
        )

        merged_pdf.seek(0)

        doc=fitz.open(stream=merged_pdf.read(),filetype="pdf")

        st.header("Preview")

        for page in doc:

            pix=page.get_pixmap(matrix=fitz.Matrix(2,2))

            img=pix.tobytes("png")

            st.image(img,
                     caption=f"Page {page.number+1}",
                     use_container_width=True)

        doc.close()
