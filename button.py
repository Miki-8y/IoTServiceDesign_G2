#不完全なソースコード
#button_all.py
import RPi.GPIO as GPIO
import time
# ボタンの状態とプログラムの状態を追跡する変数
start_button_pressed = False
suction_button_pressed = False
program_running = False
start_time = None
# ボタン押下を検出する関数
def start_button_pressed_callback(channel):
    global start_button_pressed
    start_button_pressed = True
def btnPush(BtnCount):
    print ('ボタンが',BtnCount,'回押されました')
    BtnCount += 1 # カウントを1増やす

# GPIOピンの設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(24, GPIO.FALLING, callback=start_button_pressed_callback, bouncetime=200)
GPIO.add_event_detect(18, GPIO.FALLING, bouncetime=200)   #18番ピンのイベントを検知 GPIO.FALLINGはイベントの立ち下がり。 検知したら「chgLed」を実行。ご認識を防ぐため200ミリ秒連続実行を制御
try:
    BtnCount =  0
    while True:
        if start_button_pressed:
            start_button_pressed = False
            if not program_running:
                # プログラムを開始し、開始時刻を記録
                start_time = time.time()
                program_running = True
                print("プログラムを開始しました。")
                while True:
                    if suction_button_pressed:
                        start_button_pressed = False
                        if not program_running:
                            print(BtnCount)
                            btnPush(BtnCount)
            else:
                # プログラムを終了し、経過時間を表示
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(f"プログラムを終了しました。経過時間: {elapsed_time:.2f}秒")
                break
        time.sleep(0.1)
except KeyboardInterrupt:
    print("プログラムが中断されました。")
finally:
    GPIO.cleanup()