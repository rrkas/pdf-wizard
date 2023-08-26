import os
from pathlib import Path
from PyPDF2 import PdfWriter, PdfReader


def delete_selected_pages(pdf_path: Path, page_num_list: list, out_path: Path):
    inputpdf = PdfReader(open(pdf_path, "rb"))

    page_num_list.sort()
    pages = inputpdf.pages
    output = PdfWriter()
    for i, page in enumerate(pages):
        if (i + 1) not in page_num_list:
            output.add_page(page)

    if isinstance(out_path, str):
        out_path = Path(out_path)

    os.makedirs(out_path.parent, exist_ok=True)
    with open(out_path, "wb") as outputStream:
        output.write(outputStream)
