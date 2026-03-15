import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd

st.title("图片主色分析与Pantone色号匹配")

uploaded_file = st.file_uploader("上传图片", type=["jpg", "jpeg", "png"])

# 正确读取 CSV，字段名完全一致
pantone_file = "pantone-list_Version2.csv"
try:
    pantone_data = pd.read_csv(pantone_file, delimiter="\t")  # 如果是Tab分隔，用delimiter="\t"
    pantone_data.columns = pantone_data.columns.str.strip()   # 去除首尾空格
except Exception as e:
    st.error(f"Pantone色号CSV读取失败：{e}")
    st.stop()

def closest_pantone(rgb, pantone_list):
    min_dist = float('inf')
    closest_name = None
    for col in ["RED", "GREEN", "BLUE"]:
        if col not in pantone_list.columns:
            st.error(f"CSV未找到列：{col}，请检查表头为PANTONENAME\tUNIQUECODE\tRED\tGREEN\tBLUE，并用Tab分隔。")
            st.stop()
    for idx, row in pantone_list.iterrows():
        pantone_rgb = np.array([row["RED"], row["GREEN"], row["BLUE"]])
        dist = np.linalg.norm(np.array(rgb) - pantone_rgb)
        if dist < min_dist:
            min_dist = dist
            closest_name = row["PANTONENAME"]
    return closest_name

if uploaded_file:
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption="上传的图片")
        image = image.convert("RGB")
        pixels = np.array(image).reshape(-1, 3)
        avg_rgb = pixels.mean(axis=0).astype(int)
        pantone_result = closest_pantone(avg_rgb, pantone_data)
        st.write(f"主色RGB: {avg_rgb.tolist()}")
        st.write(f"最接近Pantone色号: {pantone_result}")
    except Exception as e:
        st.error(f"图片分析失败: {e}")