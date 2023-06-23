from flask import Flask, render_template, request, redirect, url_for
import os
from database import getMySqlConnection
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/images'


@app.route("/")  # rute yang di akses di url
def index():  # fungsi yang dipanggil sesuai dengan url diatas
    db = getMySqlConnection()  # fungsi yang dipanggil sesuai dengan url diatas
    sqlstr = f"SELECT * from menu"
    cur = db.cursor()
    cur.execute(sqlstr)
    output_json = cur.fetchall()
    print(output_json)
    return render_template('home.html', menu=output_json)


@app.route("/detail/<int:menu_id>")
def detail(menu_id):
    db = getMySqlConnection()  # fungsi yang dipanggil sesuai dengan url diatas
    sqlstr = f"SELECT * from menu where id = {menu_id}"
    cur = db.cursor()
    cur.execute(sqlstr)
    output_json = cur.fetchall()
    print(output_json)
    return render_template('detail_page.html', menu=output_json)


@app.route("/delete/<int:menu_id>")
def delete(menu_id):
    db = getMySqlConnection()  # fungsi yang dipanggil sesuai dengan url diatas
    sqlstr = f"DELETE from menu where id = {menu_id}"
    cur = db.cursor()
    cur.execute(sqlstr)
    db.commit()
    cur.close()
    return redirect(url_for('index'))

# rute yang di akses di url


@app.route("/tambah_menu", methods=['POST', 'GET'])
def tambah_menu():  # fungsi yang dipanggil sesuai dengan url diatas
    db = getMySqlConnection()  # fungsi yang dipanggil sesuai dengan url diatas
    if request.method == "POST":
        data = request.form.to_dict()
        file = request.files['gambar_menu']
        data['gambar_menu'] = file.filename
        if file == None:
            print("WKWKWK")
        print(data)
        try:
            cur = db.cursor()
            sqlstr = f"INSERT INTO menu (nama_menu, deskripsi, alamat_gambar) VALUES('{data['nama_menu']}', '{data['deskripsi']}', '{data['gambar_menu']}')"
            cur.execute(sqlstr)
            db.commit()
            cur.close()
            file.save(os.path.join('static/images', file.filename))

            print('sukses')
            # output_json = cur.fetchall()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('index'))
    return render_template('add_menu.html')


@app.route("/update/<int:menu_id>", methods=['POST', 'GET'])
def update(menu_id):  # fungsi yang dipanggil sesuai dengan url diatas
    db = getMySqlConnection()

    if request.method == "POST":
        data = request.form.to_dict()  # ambil data dari form

        gambarMenu = request.files['gambar_menu']  # ambil data gambar

        try:
            cur = db.cursor()

            if gambarMenu.filename:  # jika gambar di update
                print("true")

                # update nama gambar di database
                cur.execute(
                    f"UPDATE menu SET alamat_gambar = '{gambarMenu.filename}'")
                db.commit()

                # save gambar di folder images
                gambarMenu.save(os.path.join(
                    'static/images', gambarMenu.filename))

            sqlstr = f"UPDATE menu SET nama_menu = '{data['nama_menu']}', deskripsi = '{data['deskripsi']}' WHERE id = {menu_id}; "

            cur.execute(sqlstr)

            db.commit()
            cur.close()

            print('sukses')
            print(data)
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(url_for('index'))

    else:
        sqlstr = f"SELECT * from menu where id = {menu_id}"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()

        print(output_json)
        return render_template('update_form.html', data=output_json)


@app.route("/about")
def about_page():
    return render_template('about.html', title='ini judul', message='pesan di halaman about')


@app.route("/product/<int:product_id>")
def show_product(product_id):
    return f"product id: {product_id}"


if __name__ == "__main__":
    app.run(debug=True)
