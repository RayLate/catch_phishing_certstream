import os
import shutil
from PIL import Image
import cv2
import numpy as np

for folder in os.listdir('Z:\\2022-09-05'):
    shot_path = os.path.join('Z:\\2022-09-05', folder, 'shot.png')
    if not os.path.exists(shot_path):
        continue

    old_screenshot_img = Image.open(shot_path).convert("RGB")
    old_screenshot_img_arr = np.asarray(old_screenshot_img)
    old_screenshot_img_arr = np.flip(old_screenshot_img_arr, -1)  # RGB2BGR
    img = cv2.cvtColor(old_screenshot_img_arr, cv2.COLOR_BGR2GRAY)

    img_area = np.prod(img.shape)
    white_area = np.sum(img == 255)
    if white_area / img_area >= 0.9:  # skip white screenshots
        shutil.rmtree(os.path.join('Z:\\2022-09-05', folder))