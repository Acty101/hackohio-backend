import os
import uuid
from flask import Flask, request
from yolo_model import DetectModel
from langChain import LangChainURL, LangChainOutput
from shared_utils import generate_file_from_output, get_prompt
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

    ##### OBJECT DETECTION MODEL #####
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
    ##### LANGCHAIN #####
    # generate supercategories using LangChain
    prompt = get_prompt(
        os.path.join(config_folder, "prompt.txt"),
        os.path.join(config_folder, "supercategory.yaml"),
    )
    if content["url"]:
        langchain = LangChainURL(prompt, url=[content["url"]])
    else:
        # no url key
        langchain = LangChainURL(
            prompt,
            url=[
                "https://www.a2gov.org/departments/trash-recycling/pages/recycling.aspx"
            ],
        )

    # create names for langchain
    names = []
    for item in result:
        names.append(item["name"])
    print(names)
    lc_result = langchain.infer(names)
    # order of lc_result is consistent with order of inputs
    for i, triplets in enumerate(lc_result):
        print(triplets)
        print(i)
        supercategory = triplets[LangChainOutput.SUPERCATEGORY]
        result[i]["supercategory"] = supercategory
        result[i]["instructions"] = triplets[LangChainOutput.INSTRUCTIONS]
    print(result)
    ##### UPLOAD #####
    # upload markers

    category_id = {}
    try:
        if content["geolocation"]:
            location = content["geolocation"]
            sc_count = langchain.sc_count
            table_name = os.environ.get("DYDB_TABLE")
            dydb = DYDB(table_name)
            for key, value in sc_count.items():
                id = str(uuid.uuid4())
                data = {
                    "id": id,
                    "location": location,
                    "supercategory": key,
                    "instances": value,
                }
                dydb.create(data)
                category_id[key] = id
    except:
        print("Failed to upload. HELP!!!")
    
    return {"items": result, "id": category_id}
