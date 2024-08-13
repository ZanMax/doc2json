from fastapi import FastAPI, File, UploadFile
from docx import Document
import PyPDF2
import textract

app = FastAPI()


@app.post("/parse_document")
async def parse_document(file: UploadFile = File(...)):
    file_extension = file.filename.split(".")[-1].lower()
    content = None

    if file_extension == "doc":
        content = parse_doc(await file.read())
    elif file_extension == "docx":
        content = parse_docx(await file.read())
    elif file_extension == "pdf":
        content = parse_pdf(await file.read())
    elif file_extension == "txt":
        content = parse_txt(await file.read())
    elif file_extension == "rtf":
        content = parse_rtf(await file.read())
    else:
        return {"error": "Unsupported file format"}

    return {"content": content}


def parse_doc(file_bytes):
    # Use textract to parse .doc files since python-docx does not support .doc
    text = textract.process(file_bytes, extension='doc')
    return text.decode('utf-8')


def parse_docx(file_bytes):
    # Use python-docx to parse .docx files
    from io import BytesIO
    doc = Document(BytesIO(file_bytes))
    full_text = []
    for paragraph in doc.paragraphs:
        full_text.append(paragraph.text)
    return '\n'.join(full_text)


def parse_pdf(file_bytes):
    # Use PyPDF2 to parse .pdf files
    from io import BytesIO
    reader = PyPDF2.PdfReader(BytesIO(file_bytes))
    full_text = []
    for page in reader.pages:
        full_text.append(page.extract_text())
    return '\n'.join(full_text)


def parse_txt(file_bytes):
    # Use built-in Python functions to parse .txt files
    return file_bytes.decode('utf-8')


def parse_rtf(file_bytes):
    # Use textract to parse .rtf files
    text = textract.process(file_bytes, extension='rtf')
    return text.decode('utf-8')
