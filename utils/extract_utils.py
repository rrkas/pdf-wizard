import os
from pathlib import Path
from PyPDF2 import PdfWriter, PdfReader


def extract_selected_pages(pdf_path: Path, page_num_list: list, out_path: Path):
    inputpdf = PdfReader(open(pdf_path, "rb"))

    page_num_list.sort()
    pages = inputpdf.pages
    output = PdfWriter()
    for i, page in enumerate(pages):
        if (i + 1) in page_num_list:
            output.add_page(page)

    if isinstance(out_path, str):
        out_path = Path(out_path)

    os.makedirs(out_path.parent, exist_ok=True)
    with open(out_path, "wb") as outputStream:
        output.write(outputStream)


def extract_all_pages(pdf_path: Path, out_dir: Path, prefix="Document-"):
    os.makedirs(out_dir, exist_ok=True)
    inputpdf = PdfReader(open(pdf_path, "rb"))
    pages = inputpdf.pages
    idx_width = len(str(len(pages)))
    for page_idx, page in enumerate(pages):
        output = PdfWriter()
        output.add_page(page)
        with open(
            out_dir / f"{prefix}{str(page_idx + 1).zfill(idx_width)}.pdf",
            "wb",
        ) as outputStream:
            output.write(outputStream)
