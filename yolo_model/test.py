if __name__ == "__main__":
    from main import DetectModel
    from PIL import Image
    img = "./test_images/1.jpg"

    det_model = DetectModel()
    # 1.jpg -> 800 x 536
    print(det_model.predict(img))





