import RPi.GPIO as GPIO
import time

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
GPIO.add_event_detect(21, GPIO.FALLING,callback=suction_button_pressed_callback, bouncetime=200)   #18番ピンのイベントを検知 GPIO.FALLINGはイベントの立ち下がり。 検知したら「chgLed」を実行。ご認識を防ぐため200ミリ秒連続実行を制御

try:
    while True:
        # 開始ボタンを押下したら
        if start_button_pressed:
            suction_button_count = 0
            start_button_pressed = False
            if not program_running:
                # プログラムを開始し、開始時刻を記録
                start_time = time.time()
                print("プログラムを開始しました。")
                while True:
                    # 吸引回数ボタンを押下したら
                    if suction_button_pressed:
                        suction_button_count += 1
                        print(suction_button_count)
                        suction_button_pressed = False
                    elif start_button_pressed:
                        # プログラムを終了し、経過時間を表示
                        end_time = time.time()
                        elapsed_time = end_time - start_time
                        print(f"吸引回数測定を終了しました。経過時間: {elapsed_time:.2f}秒")
                        break
                program_running = True
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