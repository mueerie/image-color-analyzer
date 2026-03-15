import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd

st.title("图片主色分析+Pantone色号查询")
uploaded_file = st.file_uploader("上传图片", type=["jpg", "png"])

pantone_data = pd.read_csv("pantone-list_Version2.csv")

def closest_pantone(rgb, pantone_list):
    min_dist = float('inf')
    closest = None
    for idx, row in pantone_list.iterrows():
        dist = np.linalg.norm(np.array(rgb) - np.array(row[['R', 'G', 'B']]))
        if dist < min_dist:
            min_dist = dist
            closest = row['Pantone']
    return closest

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="上传的图片")
    pixels = np.array(image).reshape(-1, 3)
    avg_rgb = pixels.mean(axis=0).astype(int)
    pantone_result = closest_pantone(avg_rgb, pantone_data)
    st.write(f"主色RGB: {avg_rgb.tolist()}")
    st.write(f"最接近Pantone色号: {pantone_result}")
