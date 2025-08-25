import requests
import os

# URL của FastAPI service (phải đang chạy thì test mới pass)
FASTAPI_URL = "http://localhost:30000"   # nếu chạy local thì đổi obj-service -> localhost

def test_inference_returns_poly_and_score():
    # Gán cứng đường dẫn ảnh test
    img_path = "images/boats.jpg"   # bạn tạo folder tests/data và bỏ 1 ảnh jpg vào đó

    # Mở ảnh để gửi
    with open(img_path, "rb") as f:
        files = {"file": f}
        response = requests.post(f"{FASTAPI_URL}/cache_inference", files=files)

    # Kiểm tra API trả về status 200
    assert response.status_code == 200, f"API failed: {response.text}"

    result = response.json()

    # Kiểm tra response có bbox và score
    assert "bbox" in result, "Result missing bbox"
    assert "score" in result, "Result missing score"

    # Kiểm tra định dạng bbox là list các polygon (list of list)
    assert isinstance(result["bbox"], list)
    assert all(isinstance(poly, list) for poly in result["bbox"])

    # Kiểm tra score là list số
    assert isinstance(result["score"], list)
    assert all(isinstance(s, (int, float)) for s in result["score"])

    print("✅ Inference API trả về bbox và score hợp lệ!")
