import numpy as np
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


def preprocess_data(img_path, width, height):
    img = Image.open(img_path).convert('RGB')
    w, h = img.size
    if w > width or h > height:
        scale = min(width / w, height / h)
        w = int(scale * w)
        h = int(scale * h)
        img = img.resize((w,h))

    img_padded = np.zeros((height, width, 3), dtype=np.byte)
    img_padded[:h, :w] = np.array(img, dtype=np.byte)
    return img_padded

