import cv2
import numpy as np
from ultralytics import YOLO
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from loguru import logger
# from predict import visualize_obb
from typing import Annotated
from io import BytesIO
from fastapi import UploadFile, File
import imagehash
from PIL import Image


cache = {}
app = FastAPI(root_path="/")
model = YOLO("yolo11n-obb.pt")

@app.get("/metadata")
def get_metadata():
    return { "app": "this is my app metadata"}

@app.post("/inference")
async def infer(file: UploadFile = File(...)):
    logger.info(f"READ FILE")
    request_object = await file.read()
    nparr = np.frombuffer(request_object, np.uint8)  # bytes -> NumPy array
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)   # array -> OpenCV image
    
    logger.info(f"PREDICT FILE")
    results = model(image)
    
    final = {"bbox": [], "score": [], "class": []}
    for result in results:
        xyxyxyxy = result.obb.xyxyxyxy.cpu().numpy()  # (N, 4, 2)
        confs = result.obb.conf.cpu().numpy()
        names = [result.names[int(cls)] for cls in result.obb.cls.int().cpu().numpy()]
        for poly, conf, name in zip(xyxyxyxy, confs, names):
            final["bbox"].append(poly.tolist())
            final["score"].append(float(conf))
            final["class"].append(name)
    return final 

@app.post("/cache_inference")
async def infer(file: UploadFile = File(...)):
    logger.info(f"READ FILE")
    request_object = await file.read()
    nparr = np.frombuffer(request_object, np.uint8)  # bytes -> NumPy array
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)   # array -> OpenCV image

    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    pil_hash = imagehash.average_hash(pil_image)
    
    logger.info(pil_hash)

    if pil_hash in cache:
        logger.info("Getting result from cache!")
        return cache[pil_hash]
    else:
        logger.info(f"PREDICT FILE")
        results = model(image)
        
        final = {"bbox": [], "score": [], "class": []}
        for result in results:
            xyxyxyxy = result.obb.xyxyxyxy.cpu().numpy()  # (N, 4, 2)
            confs = result.obb.conf.cpu().numpy()
            names = [result.names[int(cls)] for cls in result.obb.cls.int().cpu().numpy()]
            for poly, conf, name in zip(xyxyxyxy, confs, names):
                final["bbox"].append(poly.tolist())
                final["score"].append(float(conf))
                final["class"].append(name)

        cache[pil_hash] = final
        return final