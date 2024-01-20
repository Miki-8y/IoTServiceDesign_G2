import pymysql.cursors
import datetime

# ボタンに関するモジュール
import RPi.GPIO as GPIO
import time

# カメラに関するモジュール
import cv2

# ボタンの状態とプログラムの状態を追跡する変数
# 開始ボタン
start_button_pressed = False
# 吸引回数ボタン
suction_button_pressed = False
program_running = False
start_time = None

# 開始ボタン押下を検出する関数
def start_button_pressed_callback(chanel):
    global start_button_pressed
    start_button_pressed = True
    
# 吸引回数ボタン押下を検知する関数
def suction_button_pressed_callback(chanel):
    global suction_button_pressed
    suction_button_pressed = True

# GPIOピンの設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(20, GPIO.FALLING, callback=start_button_pressed_callback, bouncetime=200)
GPIO.add_event_detect(21, GPIO.FALLING,callback=suction_button_pressed_callback, bouncetime=200)

# 吸引回数，銘柄取得関数
# def equit():
#     global suction, brand

# equitdb（データベース）のequittbl（テーブル）に喫煙データを格納
def input_data(start_time,end_time,suction,brand):
    
    #******　ダミーデータ（実際は，ボタンが押されたら実行される）******
    username = 'こまつ'
    #**************************************************************
    
    # 喫煙開始・終了（年月日時間分）
    suctiontime_start = start_time
    suctiontime_end = end_time
    
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO equittbl(username, suctiontime_start, suctiontime_end, suction, brand) VALUES(%s,%s,%s,%s,%s)"
            cursor.execute(sql,(username,suctiontime_start,suctiontime_end,suction,brand))
            connection.commit()
            print("Data commited!")
    except:
        print("DB Access Error...")
        
connection = pymysql.connect(host="localhost", user="ty", password="ty2024", db="equitdb", charset="utf8")

#main関数
if __name__ == '__main__':
    # equit()
    
    suction_button_count = 0
    
    # **********喫煙開始・終了，吸引回数取得**********
    try:
        while True:
            # 開始ボタンを押下したら
            if start_button_pressed:
                start_button_pressed = False
                if not program_running:
                    # プログラムを開始し、開始（年月日 時間分）を記録
                    start_time = datetime.datetime.today()
                    print("プログラムを開始しました．")
                    while True:
                        # 吸引回数ボタンを押下したら
                        if suction_button_pressed:
                            suction_button_count += 1
                            print(suction_button_count)
                            suction_button_pressed = False
                        elif start_button_pressed:
                            # プログラムを終了し、終了（年月日 時間分）を記録
                            # 経過時間を表示
                            end_time = datetime.datetime.today()
                            print("吸引回数測定を終了しました．")
                            break
                    program_running = True
                else:
                    print("プログラムを終了しました．")
                    break
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("プログラムが中断されました。")
    finally:
        GPIO.cleanup()
    # **********************************
    
    # 吸引回数
    suction = suction_button_count
    
    #*******カメラのキャプチャを開始******
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
    
    # 銘柄
    brand=decodedText
    # ***********************************************
    
    input_data(start_time,end_time,suction,brand)

connection.close()