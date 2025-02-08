import streamlit as st
import cv2
import numpy as np

# QRコード検出器をロード
@st.cache_resource
def load_qrcode_detector():
    qrcode_detector = cv2.QRCodeDetector()
    return qrcode_detector

# カメラから画像を取得
img_file_buffer = st.camera_input("ボタンを押してQRコードをスキャンしてください", label_visibility="collapsed")

if img_file_buffer is not None:
    # OpenCV形式の画像データに変換する
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    # QRコードを検出
    qrcode_detector = load_qrcode_detector()
    detected, decoded_info, points, _ = qrcode_detector.detectAndDecodeMulti(cv2_img)

    if detected:
        # QRコードの情報が読み取れているかどうか確認
        count = 0
        for data in decoded_info:
            if data == "":
                continue
            count += 1
        if count == 0:
            st.warning("QRコードが見つかりませんでした")
            st.stop()

        st.caption("QRコードに含まれている情報")
        idx = 0
        for data in decoded_info:
            if data == "":
                continue
            idx += 1
            st.write(f"{idx}: ", data)

        img = cv2.polylines(cv2_img, points.astype(int), True, (0, 255, 0), 3)
        st.caption("QRコードの検出結果")
        st.image(img)
    else:
        st.warning("QRコードが見つかりませんでした")
