import json, uuid, shutil
from utils import *
from utils.file_utils import get_file_name
from utils.delete_utils import delete_selected_pages
from flask import Blueprint, request, send_file

bp = Blueprint("delete_pages", __name__)


@bp.route("/pdf/delete/pages/", methods=["GET", "POST"])
def delete_pages():
    if request.method == "POST":
        files = request.files.getlist("file")
        # print(files, flush=True)
        if len(files) == 0:
            return {"error": "No `file` provided to split"}
        file = files[0]
        # print(file.filename)
        if not any([file.filename.endswith(e) for e in [".pdf", ".PDF"]]):
            return {"error": f"File {file.filename} is not a PDF (.pdf, .PDF)"}

        org_fp = UPLOADS_DIR / f"{get_file_name()}.pdf"
        file.save(org_fp)

        form = request.form

        selection = form.get("selection")

        pl = set()
        for page_e in selection.split(","):
            if "-" in page_e:
                try:
                    s, e = map(int, page_e.split("-"))
                    pl.update(list(range(s, e + 1)))
                except:
                    pass
            else:
                try:
                    pl.add(int(page_e))
                except:
                    pass

        if len(pl) > 0:
            try:
                pl = list(sorted(pl))
                out_fp = DELETE_PAGES_DIR / f"{get_file_name()}.pdf"
                delete_selected_pages(org_fp, pl, out_fp)
                return send_file(out_fp, as_attachment=True)
            except BaseException as e:
                return {"error": str(e)}
        else:
            return {"error": "No pages to delete!"}

    return {
        "form_body": {
            "file": "file to split",
            "selection": "1,3-5,8-10,15",
        },
        "response": {
            "GET": "help json",
            "POST": {
                "PDF file contents": "PDF file containing all remaining pages after deletion",
                "json": "json containing error message",
            },
        },
        "samples": [
            """curl --location 'http://localhost:5000/pdf/delete/pages/' \
--form 'file=@"/C:/Users/Dell/Downloads/sample.pdf"' \
--form 'selection="1,3-5"'""".strip()
        ],
    }
