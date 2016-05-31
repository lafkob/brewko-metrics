from flask import Flask
app = Flask(__name__)


@app.route("/")
def app_root():
    """
    Controller method for the application root.

    :return:  
    """
    return "brewkometrics"


if __name__ == "__main__":
    app.run()
