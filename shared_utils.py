import base64
import os
import yaml


def generate_file_from_output(
    b64_data: str, folder_path=f"./tmp", filename: str = "temp.jpg"
) -> str:
    """Generate image file from base_64 data at folder_path/filename. Creates new folder if not present"""
    img_path = os.path.join(folder_path, filename)
    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)
    imgdata = base64.b64decode(b64_data)
    with open(img_path, "wb") as f:
        f.write(imgdata)
    return img_path


def get_prompt(prompt_path: str, cat_path: str):
    """Configure prompt to be suitable for input to LangChainURL"""
    f = open(prompt_path, "r")
    with open(cat_path, "r") as file:
        yaml_data = yaml.safe_load(file)
    supercategories = yaml_data.get("categories")
    return f"{f.readline()}{', '.join(supercategories)}\n{f.read()}"
