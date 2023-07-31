from PIL import Image
import os
from os import listdir
import numpy as np

def center_crop(width, height, img):
    crop = np.min(img.shape[:2])
    img = img[(img.shape[0] - crop) // 2 : (img.shape[0] + crop) // 2, (img.shape[1] - crop) // 2 : (img.shape[1] + crop) // 2]
    img = Image.fromarray(img, 'RGB')
    img = img.resize((width, height), Image.LANCZOS)
    return img


resolution = 256
folder = "../filtered_data/front/"
dest_folder = "../filtered_data/front_256cropped/"

for image in os.listdir(folder):
    if (image.endswith(".png") or image.endswith(".jpg")\
        or image.endswith(".jpeg")):
        img = np.array(Image.open(folder + image))
        cropped_img = center_crop(resolution, resolution, img)
        cropped_img.save(dest_folder + image)
 
        cropped_img.close()

