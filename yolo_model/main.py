import torch
import yaml
from PIL import Image
from typing import Tuple

class DetectModel:
    def __init__(self, path: str = "./best.pt", yaml_path: str = "./taco.yaml") -> None:
        # load model with custom weighs and GPU
        self.model = torch.hub.load("ultralytics/yolov5", "custom", device=0, path=path)

        # Load the YAML file
        with open(yaml_path, "r") as file:
            yaml_data = yaml.safe_load(file)

        # Extract the class names list for mapping
        self.names = yaml_data.get("names")

    def predict(self, img_path: str) -> list:
        im = Image.open(img_path)
        self.results = self.model(img_path)
        return self._get_results(im.size)

    def _get_results(self, dimensions: Tuple[int, int]) -> list:
        width, height = dimensions[0], dimensions[1]
        df = self.results.pandas().xyxy[0]
        result_list = []
        for index, row in df.iterrows():
            bbox = [row["xmin"]/width, row["ymin"]/height, row["xmax"]/width, row["ymax"]/height]
            result_dict = {"name": self.names[row["class"]], "bbox": bbox}
            result_list.append(result_dict)
        return result_list
