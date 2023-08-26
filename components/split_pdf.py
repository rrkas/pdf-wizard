from flask import Blueprint

bp = Blueprint("split_pdf_bp", __name__)


@bp.route("/pdf/split/")
def split_pdf():
    return "SPLIT PDF"
