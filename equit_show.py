# sql使用のためのライブラリ
import pymysql.cursors
# Web表示のためのライブラリ
from flask import Flask, render_template, request, redirect

app = Flask(__name__, static_folder='./templates/images')

@app.route("/", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/output_data", methods=["POST"])
def output_data():
    username = request.form["username"]
    
    # equittblsubテーブルのレコードをequittblに格納，usernameカラムと対応付ける
    # try:
    #     with connection.cursor() as cursor:
    #         sql = "INSERT INTO equittbl(username, suctiontime_start, suctiontime_end, cigarette, suction, brand) VALUES(%s,%s,%s,%s,%s,%s)"
    #         cursor.execute(sql,(username,suctiontime_start,suctiontime_end,cigarette,suction,brand))
    #         connection.commit()
    #         print("Data commited!")
    # except:
    #     print("DB Access Error...")
    
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM equittbl"
            cursor.execute(sql)
            result = cursor.fetchall()
    except:
        print("DB Access Error...")
    
    return render_template("show_equit_data.html", username = username, equit_data = result)

connection = pymysql.connect(host="localhost", user="ty", password="ty2024", db="equitdb", charset="utf8")

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5001, debug=True)

connection.close()