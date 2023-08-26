from flask import Flask

app = Flask(__name__)


@app.route("/ping/")
def ping():
    return "PONG"


if __name__ == "__main__":
    from components.split_pdf import bp as split_pdf_bp

    app.register_blueprint(split_pdf_bp)

    app.run(debug=True, host="0.0.0.0")
