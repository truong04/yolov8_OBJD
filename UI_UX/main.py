import streamlit as st
import requests
import json
import cv2
import numpy as np
from PIL import Image
import os

FASTAPI_URL = "http://obj_module:30000"
st.title("YOLO OBB INFERENCE DEMO")

uploaded_file = st.file_uploader("upload file", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    files = {"file": uploaded_file.getvalue()}
    response = requests.post(f"{FASTAPI_URL}/cache_inference", files=files)

    if response.status_code == 200:
        result = response.json()
        st.subheader("Detection Results (JSON)")
        st.json(result)

        np_img = np.array(image.convert("RGB"))
        for poly, score, cls in zip(result["bbox"], result["score"], result["class"]):
            pts = np.array(poly, dtype=np.int32)
            cv2.polylines(np_img, [pts], isClosed=True, color=(0,255,0), thickness=2)
            cv2.putText(np_img, f"{cls} {score:.2f}", tuple(pts[0]),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)
        st.image(np_img, caption="PREDICTED IMAGE", use_column_width=True)
    else:
        st.error(f"Error {response.status_code}: {response.text}")
