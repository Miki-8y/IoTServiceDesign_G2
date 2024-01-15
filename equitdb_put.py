import pymysql.cursors
import datetime
import random
import socket

import cv2

# Web表示のためのライブラリ
from flask import Flask, render_template, request, redirect

app = Flask(__name__, static_folder='./templates/images')

# タバコの本数，吸引回数，銘柄取得関数
def equit():
    global cigarette, suction, brand
    
    cigarette=int(1)
    suction=int(14)
    
    # カメラのキャプチャを開始
    cap = cv2.VideoCapture(0)
    # QRコード検出用のデコーダーを作成
    qrCodeDetector = cv2.QRCodeDetector()
    while True:
        # カメラから画像を読み込む
        _, frame = cap.read()
        # QRコードの検出とデコード
        decodedText, points, _ = qrCodeDetector.detectAndDecode(frame)
        if points is not None:
            # QRコードの内容が検出された場合、内容を出力
            print(decodedText)
            break  # QRコードを読み取ったらループを抜ける
        # 'q'キーが押されたらループを抜ける
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # キャプチャを解放
    cap.release()
    cv2.destroyAllWindows()  # ウィンドウを閉じる
    
    brand=decodedText
    
    #if(startendスイッチが押されたら):
        # cigarette=int(1)
        # suction=int(14)
        # brand='テリア リッチ レギュラー'
        #if(startendスイッチがもう一度押されたら)
        # break

# equitdb（データベース）のequittbl（テーブル）に喫煙データを格納
def input_data(username):
    # タバコの本数，吸引回数，銘柄
    global cigarette, suction, brand
    #id = socket.gethostname()
    #******　ダミーデータ（実際は，ボタンが押されたら実行される）******
    suctiontime_start = datetime.datetime.today()
    suctiontime_end = datetime.datetime.today()
    #**************************************************************
    #print('DateTime=%s Cigarette=%d Suction=%d Brand=%s' %(dt,cigarette,suction,brand))
    
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO equittbl(username, suctiontime_start, suctiontime_end, cigarette, suction, brand) VALUES(%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(username,suctiontime_start,suctiontime_end,cigarette,suction,brand))
            connection.commit()
            print("Data commited!")
    except:
        print("DB Access Error...")
        
@app.route("/", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/output_data", methods=["POST"])
def output_data():
    username = request.form["username"]
    
    print(username)
    
    equit()
    input_data(username)
    
    # # タバコの本数，吸引回数，銘柄
    # global cigarette_out, suction_out, brand_out
    
    # try:
    #     with connection.cursor() as cursor:
    #         sql = "SELECT * FROM equittbl"
    #         cursor.execute(sql)
    #         result = cursor.fetchall()
    # except:
    #     print("DB Access Error...")
        
    # return render_template("show_equit_data.html", equit_data = result)
    return render_template("show_equit_data.html", username = username)

connection = pymysql.connect(host="localhost", user="ty", password="ty2024", db="equitdb", charset="utf8")

# try:
    # for count in range(10):
    #     equit()
    #     input_data()
    
    #result = output_data()
    
    # # Debug
    # print(result)
    # # 吸引開始の年月日と時分秒
    # print(result[0][0])
    # # 本数
    # print(result[0][1])
    # # 吸引回数
    # print(result[0][2])
    # # 銘柄
    # print(result[0][3])
# except KeyboardInterrupt:
#     pass

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5001, debug=True)

connection.close()