import pymysql.cursors
import datetime

# ボタンに関するモジュール
import RPi.GPIO as GPIO
import time

# カメラに関するモジュール
import cv2

# GPIOピンの設定
GPIO.setmode(GPIO.BCM)
# 開始・終了用のタクトスイッチ接続ピン設定
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# 吸引回数用のタクトスイッチ接続ピン設定
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 喫煙開始・終了（年月日 時分秒），吸引回数，銘柄取得関数
def equit():
    program_running = False
    suction = 0
    # **********喫煙開始・終了，吸引回数取得**********
    try:
        while True:
            # 開始ボタンを押下したら
            if GPIO.input(20) == GPIO.HIGH:
                if not program_running:
                    # プログラムを開始し、開始（年月日 時間分）を記録
                    start_time = datetime.datetime.today()
                    print("プログラムを開始しました．")
                    time.sleep(0.2) # チャタリング防止待ち時間
                    while True:
                        # 吸引回数ボタンを押下したら
                        if GPIO.input(21) == GPIO.HIGH:
                            suction += 1
                            print(suction)
                            time.sleep(0.2) # チャタリング防止待ち時間
                        elif GPIO.input(20) == GPIO.HIGH:
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
        
    # **********カメラのキャプチャを開始**********
    cap = cv2.VideoCapture(0)
    # QRコード検出用のデコーダーを作成
    qrCodeDetector = cv2.QRCodeDetector()
    print("QRコードを読み取ってください．")
    while True:
        # カメラから画像を読み込む
        _, frame = cap.read()
        # QRコードの検出とデコード
        decodedText, points, _ = qrCodeDetector.detectAndDecode(frame)
        print(points)
        if points is not None:
            # QRコードの内容が検出された場合、内容を出力
            print(decodedText)
            if decodedText == '':
                decodedText = "None"
            break  # QRコードを読み取ったらループを抜ける
        else:
            decodedText = "None"
        # # 'q'キーが押されたらループを抜ける
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
    # キャプチャを解放
    cap.release()
    cv2.destroyAllWindows()  # ウィンドウを閉じる
    
    return start_time,end_time,suction,decodedText
    # *******************************************

# equitdb（データベース）のequittbl（テーブル）に喫煙データを格納
def input_data(suctiontime_start,suctiontime_end,suction,brand):
    
    #******ダミーデータ（実際は，ボタンが押されたら実行される）******
    username = 'こまつ'
    #************************************************************
    
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO equittbl(username, suctiontime_start, suctiontime_end, suction, brand) VALUES(%s,%s,%s,%s,%s)"
            cursor.execute(sql,(username,suctiontime_start,suctiontime_end,suction,brand))
            connection.commit()
            print("Data commited!")
    except:
        print("DB Access Error...")
        
connection = pymysql.connect(host="localhost", user="ty", password="ty2024", db="equitdb", charset="utf8")

# main関数
if __name__ == '__main__':    
    # 喫煙開始・終了（年月日 時分秒），吸引回数，銘柄取得
    start_time,end_time,suction,decodedText = equit()
    
    # 喫煙開始・終了（年月日時間分）
    # 小数点以下切り捨て
    start_time = start_time.replace(microsecond = 0)
    end_time = end_time.replace(microsecond = 0)

    # Debug
    # print(suction)
    # print(start_time.replace(microsecond = 0))
    # print(end_time.replace(microsecond = 0))
    # print(decodedText)
    
    input_data(start_time,end_time,suction,decodedText)

connection.close()