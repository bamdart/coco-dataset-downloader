import glob
import os
import cv2
import numpy as np 

images = glob.glob('./downloaded_images/*')

for image_file_path in images:
    image = cv2.imread(image_file_path)

    image_path, image_file_name = os.path.split(image_file_path)
    image_file_name, image_file_name_extension = os.path.splitext(image_file_name)

    label = []

    with open('./downloaded_labels/' + image_file_name + '.txt', 'r', encoding='utf-8') as f:
        label = eval(f.read())

    top, left, bottom, right = label[-4:]

    print(image_file_name, label, top, left, bottom, right)

    top = int(top)
    left = int(left)
    bottom = int(bottom)
    right = int(right)

    cv2.imwrite('./splited_images/' + image_file_name + image_file_name_extension, image[top:bottom, left:right])
    cv2.waitKey(0)