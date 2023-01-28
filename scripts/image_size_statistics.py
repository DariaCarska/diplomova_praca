import os
from PIL import Image
import operator

from constants import VIEWS


def get_statistics():
    dict_dimensions = {}
    dict_ratios = {}

    for dir in os.listdir('../raw_data/Invisalign/'):
        for img_file in os.listdir('../raw_data/Invisalign/' + dir):
            if any(view in img_file for view in VIEWS):
                try:
                    img = Image.open(os.path.join('../raw_data/Invisalign', dir, img_file))
                except:
                    print("Wrong image file (" + img_file + ")")
                    continue

                ratio = img.size[0] / img.size[1]
                ratio = round(ratio, 2)

                dict_ratios[ratio] = dict_ratios.get(ratio, 0) + 1
                if ratio not in dict_dimensions.keys():
                    dict_dimensions[ratio] = {}
                dict_dimensions[ratio][img.size] = dict_dimensions[ratio].get(img.size, 0) + 1

    sorted_dict_ratios = sorted(dict_ratios.items(), key=operator.itemgetter(1), reverse=True)
    result_ratio = sorted_dict_ratios[0][0]

    sorted_dimensions = sorted(dict_dimensions[result_ratio].items(), key=operator.itemgetter(1), reverse=True)
    result_dimension = sorted_dimensions[0][0]

    return (result_dimension[0] // 10, result_dimension[1] // 10)


print(get_statistics())
