import os
from pathlib import Path

MEDIA_PATH = Path("media/")
UPLOADS_DIR = MEDIA_PATH / "uploaded_files"

# feature wise
SPLIT_PDF_DIR = MEDIA_PATH / "splitted_PDFs"
MERGE_PDF_DIR = MEDIA_PATH / "merged_PDFs"
DELETE_PAGES_DIR = MEDIA_PATH / "delPages_PDFs"


for e in [
    MEDIA_PATH,
    UPLOADS_DIR,
    SPLIT_PDF_DIR,
    MERGE_PDF_DIR,
    DELETE_PAGES_DIR,
]:
    os.makedirs(e, exist_ok=True)
