#!/usr/bin/env python3
# -*- coding: utf-8 -*-

HEIGHT = 256
WIDTH = 256

from PIL import Image
import numpy as np

def preprocess_data(img_path):
    img = Image.open(img_path)
    img_gray = img.convert('L')
    
    w, h = img.size
    if w > WIDTH or h > HEIGHT:
        scale = min(WIDTH / w, HEIGHT / h)
        new_w = int(np.floor(scale * w))
        new_h = int(np.floor((scale * h)))
        img_scaled = img_gray.resize((new_w, new_h))
    
    img_padded = np.zeros((WIDTH, HEIGHT), dtype = np.int)
    img_padded[:new_h, :new_w] = np.array(img_scaled)
    return img_padded