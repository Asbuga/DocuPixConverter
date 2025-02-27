"""Домашнє завдання 11

11.2 Зробити конвертор для docx або doc у pdf та навпаки
"""

from typing import Union

from docx import Document
from fpdf import FPDF
from PyPDF2 import PdfReader


def _read_docx(filename: Union[str, bytes]) -> str:
    """Reads DOCX file and return only text content.

    Args:
        filename (Union[str, bytes]): filename or file path

    Returns:
        str: file content
    """
    document = Document(filename)
    return "\n".join([line.text for line in document.paragraphs])


def write_docx(filename: Union[str, bytes], content: str) -> None:
    """Writes textual content to a DOCX file.

    Args:
        filename (Union[str, bytes]): filename or file path
        content (str): textual content to write to a DOCX file
    """
    document = Document()
    for line in content.split("\n"):
        document.add_paragraph(line)
    document.save(filename)


def _read_pdf(filename: Union[str, bytes]) -> str:
    """Reads DOCX file and return only text content.

    Args:
        filename (Union[str, bytes]): filename or file path

    Returns:
        str: file content
    """
    reader = PdfReader(stream=filename)
    return "\n".join(
        [reader.pages[i].extract_text() for i in range(0, len(reader.pages))]
    )


def write_pdf(filename: Union[str, bytes], content: str) -> None:
    """Writes textual content to a PDF file.

    Args:
        filename (Union[str, bytes]): filename or file path
        content (str): textual content to write to a PDF file
    """
    pdf = FPDF()
    pdf.set_font("Arial", size=12)
    pdf.add_page()
    pdf.write(5, content)
    pdf.output(filename)


if __name__ == "__main__":
    # Let's set the path to the files for the presentation
    file_docs = ".\\data\\data.docx"
    file_pdf = ".\\data\\data.pdf"
    _file_to_docs = ".\\data\\to_docx.docx"

    # Convert DOCX to PDF
    write_pdf(filename=file_pdf, content=_read_docx(file_docs))
    print("Convert DOCX to PDF is successfully!")

    # Convert PDF to DOCX
    write_docx(filename=_file_to_docs, content=_read_pdf(file_pdf))
    print("Convert PDF to DOCX is successfully!")
