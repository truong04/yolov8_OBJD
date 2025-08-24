import cv2
import numpy as np
from ultralytics import YOLO
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from loguru import logger

model = YOLO("yolo11n-obb.pt")

def visualize_obb(img_path, output_path):
    # Đọc ảnh
    image = cv2.imread(img_path)
    if image is None:
        raise FileNotFoundError(f"Không tìm thấy ảnh: {img_path}")
   
    results = model(img_path)
    if output_path is None:
        output_path = "result.jpg"
    for result in results:
        xyxyxyxy = result.obb.xyxyxyxy.cpu().numpy()  # (N, 4, 2)
        confs = result.obb.conf.cpu().numpy()
        names = [result.names[int(cls)] for cls in result.obb.cls.int().cpu().numpy()]

        for poly, conf, name in zip(xyxyxyxy, confs, names):
            poly = np.array(poly, dtype=np.int32)
            cv2.polylines(image, [poly], isClosed=True, color=(0, 255, 0), thickness=2)
            text = f"{name} {conf:.2f}"
            cv2.putText(
                image,
                text,
                (int(poly[0][0]), int(poly[0][1]) - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

    cv2.imwrite(output_path, image)
    print(f"✅ Saved visualized result to {output_path}")
    return output_path

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Visualize OBB predictions from YOLO model.")
    parser.add_argument("--img_path", type=str, help="Path to the input image.")
    parser.add_argument("--output_path", type=str, default=None, help="Path to save the output image with OBBs.")

    args = parser.parse_args()
    if args.output_path is None:
        output = "result.jpg"
    else:
        output = args.output_path
    visualize_obb(args.img_path, output)