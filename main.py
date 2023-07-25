from flask import Flask
from zpool import fake_zpool, get_zpool

app = Flask(__name__)


def wrap(text):
    return f"<pre>{text}</pre>"


@app.route("/")
def test():
    return wrap("".join(get_zpool()))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000, debug=True)
