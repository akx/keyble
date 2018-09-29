import tesserocr


def get_textlines(pil_image):
    with tesserocr.PyTessBaseAPI() as api:
        api.SetImage(pil_image)
        boxes = api.GetComponentImages(tesserocr.RIL.TEXTLINE, True)
        for i, (im, box, _, _) in enumerate(boxes):
            api.SetRectangle(box['x'], box['y'], box['w'], box['h'])
            text = api.GetUTF8Text().strip()
            if not text:
                continue
            yield {
                'box': box,
                'confidence': api.MeanTextConf(),
                'text': text,
                'image': im,
            }


def ocr_card(pil_image):
    lines = list(get_textlines(pil_image))
    lines.sort(key=lambda b: b['box']['y'])
    return {
        'image_size': pil_image.size,
        'lines': lines,
    }
