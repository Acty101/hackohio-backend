import torch
import yaml


class DetectModel:
    def __init__(self, path: str, yaml_path: str) -> None:
        # load model with custom weighs and GPU
        self.model = torch.hub.load("ultralytics/yolov5", "custom", device=0, path=path)

        # Load the YAML file
        with open(yaml_path, "r") as file:
            yaml_data = yaml.safe_load(file)

        # Extract the class names list for mapping
        self.names = yaml_data.get("names")

    def predict(self, img_path: str) -> None:
        self.results = self.model(img_path)

    def get_results(self):
        df = self.results.pandas().xyxy[0]
        result_list = []
        for index, row in df.iterrows():
            bbox = [row["xmin"], row["ymin"], row["xmax"], row["ymax"]]
            result_dict = {"name": self.names[row["class"]], "bbox": bbox}
            result_list.append(result_dict)
        return result_list
