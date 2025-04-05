import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
from predictor import predict

# タイトル
st.title("アノテーションアプリ")

# 画像の読み込み
image = Image.open("sample.jpg")  # 任意の画像ファイルに置き換えてください
# アスペクト比を維持してリサイズ
image.thumbnail((600, 600))

if "image" not in st.session_state:
    st.session_state["image"] = image

# キャンバス設定
st.write("画像上をクリックしてください")

canvas_result = st_canvas(
    fill_color="rgba(255, 0, 0, 1)",
    stroke_width=5,
    stroke_color="red",
    background_image=st.session_state["image"],
    update_streamlit=True,
    height=image.height,
    width=image.width,
    drawing_mode="point",
    key="canvas",
)

# 座標の取得と表示
if canvas_result.json_data is not None:
    objects = canvas_result.json_data["objects"]
    if objects:
        point_coords = []
        for i, obj in enumerate(objects):
            x = int(obj["left"])
            y = int(obj["top"])
            point_coords.append([x, y])

        try:
            # detector.pyのpredict関数を呼び出す
            mask = predict(image, point_coords=point_coords)

            # マスクを画像に重ねて表示
            overlay_image = np.array(image)
            overlay_image[mask] = overlay_image[mask] * 0.5 + np.array([255, 0, 0]) * 0.5
            
            # PIL画像に変換してセッションステートに保存
            overlay_pil_image = Image.fromarray(overlay_image.astype(np.uint8))
            st.session_state["image"] = overlay_pil_image
        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")
    else:
        st.session_state["image"] = image
    st.rerun()
