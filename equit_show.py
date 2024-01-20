import pymysql.cursors
import datetime

# ボタンに関するモジュール
import RPi.GPIO as GPIO
import time

# カメラに関するモジュール
import cv2

# 喫煙データ取得関数記述ファイルの読み込み
import equit_put as EP

# Web表示のためのライブラリ
from flask import Flask, render_template, request, redirect

app = Flask(__name__, static_folder='./templates/images')

# equitdb（データベース）のequittbl（テーブル）に喫煙データを格納
def input_data(username,suctiontime_start,suctiontime_end,suction,brand):    
    
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO equittbl(username, suctiontime_start, suctiontime_end, suction, brand) VALUES(%s,%s,%s,%s,%s)"
            cursor.execute(sql,(username,suctiontime_start,suctiontime_end,suction,brand))
            connection.commit()
            print("Data commited!")
    except:
        print("DB Access Error...")

# equitdb（データベース）のequittbl（テーブル）の喫煙データを読み込む
def output_data():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM equittbl"
            cursor.execute(sql)
            result = cursor.fetchall()
    except:
        print("DB Access Error...")
    return result

@app.route("/", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/home", methods=["POST"])
def home():
    global username
    # ユーザー名取得
    username = request.form["username"]
    return render_template("home.html")

@app.route("/inoutput_data", methods=["POST"])
def inoutput_data():
    # GPIOピンの設定
    GPIO.setmode(GPIO.BCM)
    # 開始・終了用のタクトスイッチ接続ピン設定
    GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # 吸引回数用のタクトスイッチ接続ピン設定
    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    # 喫煙開始・終了（年月日 時分秒），吸引回数，銘柄取得
    start_time,end_time,suction,decodedText = EP.equit()
    
    # 喫煙開始・終了（年月日時間分）
    # 小数点以下切り捨て
    start_time = start_time.replace(microsecond = 0)
    end_time = end_time.replace(microsecond = 0)
    
    # Debug
    print(suction)
    print(start_time.replace(microsecond = 0))
    print(end_time.replace(microsecond = 0))
    print(decodedText)
    
    # テーブルに喫煙データ格納
    input_data(username,start_time,end_time,suction,decodedText)
    
    # テーブルから喫煙データ読み込み
    result = output_data()
    
    # レコードから，本日の日付と一致するものを参照し，
    # 今日の本数（cigarette）を計算する
    
    return render_template("show_equit_data.html", username = username, equit_data = result)

connection = pymysql.connect(host="localhost", user="ty", password="ty2024", db="equitdb", charset="utf8")

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5001, debug=True)

connection.close()