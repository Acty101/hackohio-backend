import os
import uuid
from flask import Flask, request
from yolo_model import DetectModel
from shared_utils import generate_file_from_output
from dydb import DYDB

# to allow ultralytics to load truncated images
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

app = Flask(__name__)

INFERENCE_URL = f"/upload-image"


@app.route(INFERENCE_URL, methods=["POST"])
def predict():
    if request.method != "POST":
        return

    # generate img path
    content = request.get_json()
    b64_img = content["photo"]
    img_path = generate_file_from_output(b64_img)

    # create model and run inference
    config_folder = f"./config"
    detection_model = DetectModel(
        os.path.join(config_folder, "best.pt"), os.path.join(config_folder, "taco.yaml")
    )
    result = detection_model.predict(img_path=img_path)

    # generate supercategories using LangChain


    # upload data
    # table_name = os.environ.get("DYDB_TABLE")
    # dydb = DYDB(table_name)
    # data = {"id": str(uuid.uuid4())}
    # dydb.create(data)

    # generate

    return {"items": result, "id": {}}