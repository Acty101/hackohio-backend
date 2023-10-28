# use GPU supported container
FROM nvidia/cuda:12.0.0-runtime-ubuntu20.04 as release

WORKDIR /app

# Install python deps
RUN apt-get update -y && \
	DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata && \
    apt-get install --no-install-recommends -y build-essential software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get install -y python3.9 python3-pip python3-distutils python3-venv gcc ffmpeg libsm6 libxext6 git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Object-detection + LangChain + Flask dep
COPY requirements.txt .
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt
RUN pip3 install -r https://raw.githubusercontent.com/ultralytics/yolov5/master/requirements.txt

# Copy over all files/folders
COPY dydb ./dydb/
COPY yolo_model/__init__.py yolo_model/main.py ./yolo_model/
COPY config ./config
COPY app.py shared_utils.py ./

ENTRYPOINT [ "flask", "run","--host","0.0.0.0","--port","5000"]