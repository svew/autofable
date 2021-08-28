
from PIL import Image
import os
import numpy as np
from cv2 import cv2

IMAGE_EXTENSIONS = ('.png', '.jpg')

class ImageStore:
    """Class to load templates from multiple sources, resize them to fit the game screen, and store them for quick 
    access
    """

    def __init__(self, scale_size, img_dirs=[]):
        self.__store = {}
        self.__scale_size = scale_size
        self.__img_dirs = img_dirs + [ '/config' ]

        self.__load_images()

    def get(self, name, flipped=False):
        if name in self.__store:
            name_obj = self.__store[name]
            if flipped and not name_obj['flipped']:
                self.__append_flipped_images(name_obj['list'])
                name_obj['flipped'] = True
            return name_obj['list']
        else:
            raise f'Could not find item {name} in store'

    def __load_images(self):
        for _, _, files in os.walk(IMAGES_DIR_ROOT):
            for f in files:
                if f.endswith(IMAGE_EXTENSIONS):
                    image = Image.open(f)
                    fullname = os.path.basename(os.path.splitext(f)[0])
                    l = fullname.split('_')
                    size = l[-1].split('x')
                    width = int(size[0])
                    height = int(size[1])
                    if l[-1].isdigit():
                        l = l[:-2]
                    else:
                        l = l[:-1]
                    name = str.join(l, '').lower()

                    self.__add_image(image, name, (width, height))
                    
    def __add_image(self, img, name, size):
        np_img = np.array(img)
        ratio = self.__scale_size[1] / size[1]
        dsize = (size[1] * ratio, size[0] * ratio)
        resized_img = cv2.resize(np_img, dsize)

        if name not in self.__store:
            self.__store[name] = { 'list': resized_img, 'flipped': False }
        else:
            self.__store[name]['list'].append(resized_img)

    def __append_flipped_images(self, img_list):
        for i in range(len(img_list)):
            img_list.append(cv2.flip(img_list[i], 1))

class ImageObj:
    """Class to represent an image stored in an ImageStore, scaled to the ImageStore's settings
    """

    def __init__(self, name, img, path):
        self.name = name
        self.img = img
        self.path = path