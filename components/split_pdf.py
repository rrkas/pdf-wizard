import json, uuid, shutil
from utils import UPLOADS_DIR, SPLIT_PDF_DIR
from utils.file_utils import get_file_name
from utils.extract_utils import extract_selected_pages, extract_all_pages
from flask import Blueprint, request, send_file

bp = Blueprint("split_pdf_bp", __name__)


@bp.route("/pdf/split/", methods=["GET", "POST"])
def split_pdf():
    if request.method == "POST":
        files = request.files.getlist("file")
        # print(files, flush=True)
        if len(files) == 0:
            return {"error": "No `file` provided to split"}
        file = files[0]
        print(file.filename)
        if not any([file.filename.endswith(e) for e in [".pdf", ".PDF"]]):
            return {"error": f"File {file.filename} is not a PDF (.pdf, .PDF)"}

        org_fp = UPLOADS_DIR / f"{get_file_name()}.pdf"
        file.save(org_fp)

        out_dir = SPLIT_PDF_DIR / f"{get_file_name()}"

        form = request.form

        mode = form.get("mode")
        modes = ["selected", "all"]
        if mode not in modes:
            return {"error": f"`mode` must be in {modes}"}

        selection = form.get("selection")

        if mode == "selected":
            if selection is None or len(selection) == 0:
                return {"error": f"`mode` is 'selected'; `selection` must be provided!"}
            c = 0
            for pdf_sep_e in selection.split(";"):
                pl = set()
                for page_e in pdf_sep_e.split(","):
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
                    pl = list(sorted(pl))

                    try:
                        extract_selected_pages(
                            org_fp,
                            pl,
                            out_dir / f"Document-{pdf_sep_e.replace(',', '_')}.pdf",
                        )
                        c += 1
                    except:
                        pass

            if c > 0:
                try:
                    shutil.make_archive(out_dir, "zip", out_dir)
                    return send_file(
                        str(out_dir).rstrip("/") + ".zip",
                        as_attachment=True,
                    )
                except BaseException as e:
                    return {"error": str(e)}

        elif mode == "all":
            try:
                extract_all_pages(org_fp, out_dir)
                shutil.make_archive(out_dir, "zip", out_dir)
                return send_file(
                    str(out_dir).rstrip("/") + ".zip",
                    as_attachment=True,
                )
            except BaseException as e:
                return {"error": str(e)}

        return json.loads(
            json.dumps(
                dict(
                    mode=mode,
                    selection=selection,
                    files=files,
                ),
                default=str,
            )
        )

    return {
        "file": "file to split",
        "mode": {
            "selected": "extract selected pages in PDFs",
            "all": "extract all pages in separate PDFs",
        },
        "selection": {
            "1,3-5,8-10,15;2,6-7;3,5,8": {
                "PDF 1": "contains 1,3-5,8-10,15 of original PDF",
                "PDF 2": "contains 2,6-7 of original PDF",
                "PDF 3": "contains 3,5,8 of original PDF",
            }
        },
        "samples": [
            """curl --location 'http://localhost:5000/pdf/split/' \
--form 'file=@"/C:/Users/Dell/Downloads/sample.pdf"' \
--form 'mode="selected"' \
--form 'selection="1,3-5;10-14;3-5,8,9"'""".strip()
        ],
    }
