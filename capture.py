import cv2
import sys
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
        # QRコードの周りに矩形を描画
        points = points[0]
        for i in range(4):
            pt1 = [int(val) for val in points[i]]
            pt2 = [int(val) for val in points[(i+1) % 4]]
            cv2.line(frame, pt1, pt2, (0, 255, 0), 3)
    # 画像をウィンドウに表示
    cv2.imshow('QR Code Reader', frame)
    # 'q'キーが押されたらループを抜ける
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# キャプチャを解放してウィンドウを閉じる
cap.release()
cv2.destroyAllWindows()