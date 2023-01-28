import os
import numpy as np
from matplotlib import pyplot as plt

from image_size_statistics import get_statistics
from data_preprocessing import preprocess_data
from constants import VIEWS


def load_data():
    width, height = get_statistics()
    #print(width, height)


    counter = 0
    for dir in os.listdir('../data/Invisalign'):
        for img_file in os.listdir('../data/Invisalign/' + dir):
            if any(view in img_file for view in VIEWS):
                counter += 1


    X = np.zeros((counter, height, width, 3), dtype=np.float16)
    y = np.zeros((counter, 1), dtype=np.byte)

    i = 0
    for dir in os.listdir('../data/Invisalign'):
        for img_file in os.listdir('../data/Invisalign/' + dir):
            if any(view in img_file for view in VIEWS):
                X[i] = (preprocess_data(os.path.join('../data/Invisalign', dir, img_file), width, height))
                view = [v for v in VIEWS if v in img_file][0]
                y[i] = VIEWS.index(view)
                i+=1
                #print(f'{img_file=} done')

       # if len(X) > 10:
       #     break

    #X = np.array(X, dtype=np.byte)
    #X = X.astype('float32')
    #X = X / 255.0

    #y = np.array(y)

    np.save('data_X.npy', X) # save
    np.save('data_y.npy', y)


    #plt.imshow(X[0])
    #plt.show()
    # print(X.shape)
    # print(y.shape)
    # print(y)

    return X, y

load_data()