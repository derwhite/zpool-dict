from flask import Flask
from zpool import fake_zpool, get_zpool

app = Flask(__name__)


def wrap(text):
    return f"<pre>{text}</pre>"


@app.route("/")
def test():
    return wrap("\n".join(get_zpool()))


if __name__ == "__main__":
    app.run(port=3000, debug=True)
