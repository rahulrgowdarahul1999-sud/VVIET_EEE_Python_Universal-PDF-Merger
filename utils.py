import fitz
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4
from io import BytesIO
from pypdf import PdfWriter
from docx import Document


# -----------------------------
# Convert Image -> PDF
# -----------------------------
def image_to_pdf(image_file):

    image = Image.open(image_file)

    if image.mode != "RGB":
        image = image.convert("RGB")

    pdf_bytes = BytesIO()

    image.save(pdf_bytes, format="PDF")

    pdf_bytes.seek(0)

    return pdf_bytes


# -----------------------------
# Convert DOCX -> PDF
# -----------------------------
def docx_to_pdf(docx_file):

    document = Document(docx_file)

    buffer = BytesIO()

    c = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4

    y = height - 50

    for para in document.paragraphs:

        c.drawString(40, y, para.text)

        y -= 20

        if y < 40:
            c.showPage()
            y = height - 50

    c.save()

    buffer.seek(0)

    return buffer


# -----------------------------
# Merge PDFs
# -----------------------------
def merge_pdfs(pdf_files):

    writer = PdfWriter()

    for pdf in pdf_files:

        doc = fitz.open(stream=pdf.read(), filetype="pdf")

        for page in doc:

            writer.append(doc)

        doc.close()

    merged = BytesIO()

    writer.write(merged)

    merged.seek(0)

    return merged
