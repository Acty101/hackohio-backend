from flask import Flask, request
from yolo_model import DetectModel
from shared_utils import generate_file_from_output
import os

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
    return result
    # generate supercategories using LangChain


    # generate 
