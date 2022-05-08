#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# %%
from constants import WIDTH, HEIGHT
from PIL import Image
import numpy as np

def preprocess_data(img_path):
    img = Image.open(img_path)
    img_gray = img.convert('L')
    
    w, h = img.size
    if w > WIDTH or h > HEIGHT:
        scale = min(WIDTH / w, HEIGHT / h)
        w = int(np.floor(scale * w))
        h = int(np.floor((scale * h)))
        img_gray = img_gray.resize((w, h))
    
    img_padded = np.zeros((WIDTH, HEIGHT), dtype = np.int)
    img_padded[:h, :w] = np.array(img_gray)
    return img_padded