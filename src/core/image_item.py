
from cv2 import cv2
import os
import yaml

class ImageItem:
    """Represents an image item to be found on the DragonFable screen. Item could be described with multiple items, in
    case item happens to have multiple appearances, such as an enemy
    """

    DEFAULT_CONFIDENCE = 0.95

    def __init__(self, name, cachetype='NONE', confidence=DEFAULT_CONFIDENCE):
        self.name = name
        self.image_list = [] # (image, (frame_width, frame_height))
        self.confidence = confidence
        self.cachetype = cachetype

    @staticmethod
    def load_from_folder(path):
        template_list = {}
        template_config = {}
        for dirpath, _, filenames in os.walk(path):

            # If config exists
            if 'templateconfig.yaml' in filenames:
                with open(os.path.join(dirpath, 'templateconfig.yaml'), 'r') as stream:
                    try:
                        template_config = yaml.safe_load(stream)
                    except yaml.YAMLError as e:
                        print(e)
                
            for f in filenames:
                fullname, ext = os.path.splitext(filenames)
                if ext in ['.jpg', '.png']:
                    try:
                        # two formats:
                        #     my_name_0_1980x1080 (name, numeral, size)
                        #     my_name_1980x1080 (name, size)
                        splitname = fullname.split('_')
                        sizename = splitname[-1].split('x')
                        size = (int(sizename[0]), int(sizename[1]))
                        if is_integer(splitname[-2]):
                            imgname = '_'.join(str(x) for x in splitname[:-2])
                        else:
                            imgname = '_'.join(str(x) for x in splitname[:-1])
                        
                        if imgname in template_list:
                            template = template_list[imgname]
                        elif imgname in template_config:
                            confidence = 0.95
                            if 'confidence' in template_config[imgname]:
                                confidence = template_config[imgname]['confidence']
                            cachetype = 'NONE'
                            if 'cachetype' in template_config[imgname]:
                                cachetype = template_config[imgname]['cachetype']
                            template = Template(imgname, cachetype, confidence)
                            template_list[imgname] = template
                        else:
                            template = Template(imgname)
                            template_list[imgname] = template

                        image = cv2.imread(os.path.join(dirpath, f))
                        template.image_list.append((image, size))

                    except e:
                        print(e)
                        
        return template_list

def is_integer(n):
    try:
        int(n)
    except:
        return False
    return True