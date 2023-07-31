from PIL import Image
import os
from os import listdir
 

folder = "../filtered_data/left/"
dest_folder = "../filtered_data/side/"

for image in os.listdir(folder):
    if (image.endswith(".png") or image.endswith(".jpg")\
        or image.endswith(".jpeg")):
        
        img = Image.open(folder + image)
        
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Flip the original image horizontally
        flipped_img = img.transpose(method=Image.FLIP_LEFT_RIGHT)
        flipped_img.save(dest_folder + image)
 
        img.close()
        flipped_img.close()
