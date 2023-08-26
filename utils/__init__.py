import os
from pathlib import Path

MEDIA_PATH = Path("media/")
UPLOADS_DIR = MEDIA_PATH / "uploads"

# feature wise
SPLIT_PDF_DIR = MEDIA_PATH / "split_pdf"


for e in [MEDIA_PATH, UPLOADS_DIR, SPLIT_PDF_DIR]:
    os.makedirs(e, exist_ok=True)
