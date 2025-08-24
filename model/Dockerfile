FROM python:3.9

WORKDIR /app

copy ./main.py /app
copy ./requirements.txt /app
copy ./yolo11n-obb.pt /app

RUN pip install -r requirements.txt --no-cache-dir

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "30000"]

