import os
import shutil

from constants import VIEWS

for dir in os.listdir('../raw_data/Invisalign/'):
    for img_file in os.listdir('../raw_data/Invisalign/' + dir):
        if any(view in img_file for view in VIEWS):
            print(img_file)
            view = [v for v in VIEWS if v in img_file][0]
            shutil.copy(os.path.join('../raw_data/Invisalign', dir, img_file), '../data/' + view)