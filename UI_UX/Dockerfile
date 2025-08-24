FROM python:3.9-slim AS compile-image

WORKDIR /UI_UX
# # Define virtual env
# ENV VIRTUAL_ENV=/opt/venv
# RUN python3 -m venv $VIRTUAL_ENV
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# WORKDIR /install

COPY ./requirements.txt /UI_UX

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

# FROM python:3.9-slim AS runtime-image

LABEL dev="truong"

# WORKDIR /UI_UX
# COPY --from=compile-image /opt/venv /opt/venv
COPY ./main.py /UI_UX

# Set environment variables
# ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8501

# Ref: https://github.com/mlflow/mlflow/issues/6274#issuecomment-1196106372
CMD ["streamlit", "run", "main.py"]
