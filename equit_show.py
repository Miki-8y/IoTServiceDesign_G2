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
# ログインしているユーザーの喫煙データから最新のレコードを5件取得
def output_data():
    try:
        with connection.cursor() as cursor:
            sql = "select * from equittbl where username = " + "'" + str(user_name) + "'" + "order by suctiontime_start desc limit 5"
            # sql = "select * from equittbl"
            cursor.execute(sql)
            result = cursor.fetchall()
    except:
        print("DB Access Error...")
    return result

# equitdb（データベース）のequittbl（テーブル）の喫煙データを読み込む
# ログインしているユーザの喫煙データから本日分の喫煙回数を計算
def today_cigarette_data():
    d_today = datetime.date.today()
    try:
        with connection.cursor() as cursor:
            sql = "select count(*) from equittbl where username = '" + str(user_name) + "' and suctiontime_start like '%" + str(d_today) + "%'"
            # sql = "select * from equittbl"
            cursor.execute(sql)
            today_cigarette = cursor.fetchall()
    except:
        print("DB Access Error...")
    return today_cigarette

@app.route("/", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/home", methods=["POST"])
def home():
    global user_name
    # ユーザー名取得
    user_name = request.form["username"]
    return render_template("home.html")

@app.route("/E-Quit", methods=["POST"])
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
    # print(suction)
    # print(start_time.replace(microsecond = 0))
    # print(end_time.replace(microsecond = 0))
    # print(decodedText)
    
    # テーブルに喫煙データ格納
    input_data(user_name,start_time,end_time,suction,decodedText)
    
    # result = []
    # テーブルから喫煙データ読み込み
    result = output_data()
    
    s_time_data_list = []
    e_time_data_list = []
    suction_data_list = []
    brand_data_list = []
    
    # データ整形
    for i in range(len(result)):
        s_time_data_list.append(result[i][1])
        e_time_data_list.append(result[i][2])
        suction_data_list.append(result[i][3])
        brand_data_list.append(result[i][4])
    
    # Debug
    # print(result[0])
    # print(result[0][1])
    # print(result[1][1])
    # print(result[2][1])
    # print(result[3][1])
    
    # レコードから，本日の日付と一致するものを参照し，
    # 今日の本数（cigarette）を計算する
    today_cigarette = today_cigarette_data()
    
    print(today_cigarette)
    
    return render_template("show_equit_data.html", username = user_name, equitdata_s_time = s_time_data_list, equitdata_e_time = e_time_data_list, equitdata_suction = suction_data_list, equitdata_brand = brand_data_list, equitdata_cigarette = today_cigarette)

connection = pymysql.connect(host="localhost", user="ty", password="ty2024", db="equitdb", charset="utf8")

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5001, debug=True)

connection.close()