import pymysql.cursors
import datetime
import random
import socket

# タバコの本数，吸引回数，銘柄取得関数
def equit():
    global cigarette, suction, brand
    cigarette=int(1)
    suction=int(14)
    brand='テリア リッチ レギュラー'
    

# equitdb（データベース）のequittbl（テーブル）に喫煙データを格納
def put_data():
    # タバコの本数，吸引回数，銘柄
    global cigarette, suction, brand
    #id = socket.gethostname()
    starttime = datetime.datetime.today()
    #print('DateTime=%s Cigarette=%d Suction=%d Brand=%s' %(dt,cigarette,suction,brand))
    
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO equittbl(starttime, cigarette, suction, brand) VALUES(%s,%s,%s,%s)"
            cursor.execute(sql,(starttime,cigarette,suction,brand))
            connection.commit()
            print("Data commited!")
    except:
        print("DB Access Error...")

connection = pymysql.connect(host="localhost", user="ty", password="ty2023", db="equitdb", charset="utf8")
try:
    for count in range(10):
        equit()
        put_data()
except KeyboardInterrupt:
    pass
connection.close()                