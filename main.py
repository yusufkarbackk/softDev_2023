from turtle import title
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")  # rute yang di akses di url
def index():  # fungsi yang dipanggil sesuai dengan url diatas
    return render_template('index.html')


@app.route("/about")
def about_page():
    return render_template('about.html', title='ini judul', message='pesan di halaman about')


@app.route("/product/<int:product_id>")
def show_product(product_id):
    return f"product id: {product_id}"


if __name__ == "__main__":
    app.run(debug=True)
