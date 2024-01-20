# Debug用ファイル
import cv2
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