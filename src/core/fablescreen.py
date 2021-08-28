
import time

import pyautogui
import numpy as np
from cv2 import cv2

WINDOW_BORDER_COLOR = (0, 0, 102)
CAPTURE_FREQUENCY_MS = 100
GAME_FRAME_RATIO = 1.6666

MIN_WINDOW_HEIGHT = 300
MIN_WINDOW_WIDTH = 500

GAME_FRAME_THUMBNAIL_SIZE = (333, 200) # resized image size for identifying features

FRAME_FULL = 0
FRAME_TOP = 1
FRAME_BOTTOM = 2

class FableScreen:

    def __init__(self):
        self.frame = None # Most recent capture of the screen
        self.frame_pos = None # Rect describing part of the screen where game exists. (top, left, width, height)
        self.frame_capture_time = None # Time of the most recent capture of the screen
        self.__template_cache = {}

        self.size = None # Dimensions of the game screen (width, height)

    def initialize(self):
        """Initializes the FableGame by finding the dark red border around the game.
        If the border cannot be found, initialize can be called repeatedly until the border
        is found.

        Returns:
            bool -- True if the FableGame was successfully initialized by finding the dark
            red border, false if otherwise
        """
        
        # Attempt to find the area of the screen where the DragonFable game exists
        img = np.array(pyautogui.screenshot())
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        thresh = cv2.inRange(img, WINDOW_BORDER_COLOR, WINDOW_BORDER_COLOR)

        result = self.__find_frame_hor(thresh)
        if result is None:
            result = self.__find_frame_vert(thresh)
            if result is None:
                return False

        self.frame_pos = result[:2]
        self.size = result[2:]

        return True

    def get_frame(self, view=FRAME_FULL):
        if self.__frame_pos is None:
            raise 'FableScreen not initialized'
        if self.__frame_capture_time is not None:
            next_capture = self.__frame_capture_time + CAPTURE_FREQUENCY_MS
            if next_capture < time.time_ns() // 1000000:
                return self.__frame # We have a recent frame stored
        screen = pyautogui.screenshot()
        self.frame_capture_time = time.time_ns() // 1000000
        frame_end_pos = (self.__frame_pos[0] + self.size[0], self.__frame_pos[1] + self.size[1])
        cropped = screen.crop(self.__frame_pos + frame_end_pos)
        self.__frame = cv2.cvtColor(np.array(cropped), cv2.COLOR_RGB2BGR)
        if view == FRAME_FULL:
            return self.__frame
        height = int(self.__frame.shape[1] / GAME_FRAME_RATIO)
        if view == FRAME_TOP:
            return self.__frame[:height]
        if view == FRAME_BOTTOM:
            return self.__frame[height:]
        
    def get_thumbnail(self):
        frame = self.get_frame(FRAME_TOP)
        return cv2.resize(frame, GAME_FRAME_THUMBNAIL_SIZE)

    def click_at(self, percent_pos):
        x = percent_pos[0] * self.size[0] + self.__frame_pos[0]
        y = percent_pos[1] * self.size[1] + self.__frame_pos[1]
        pyautogui.doubleClick(x, y)
        pyautogui.moveTo(10, 10)

    def click_on(self, template):
        """Click on the button with the given button name if found on the screen

        Arguments:
            button {Item} -- The visual item to be looked for on the screen

        Keyword Arguments:
            sleep {float} -- How many seconds to sleep after a successful click (default: {0})

        Returns:
            bool -- True if the button was found and clicked on, False if otherwise
        """

        pos = self.find(template)
        if pos is None:
            return False
        else:
            x, y = pos
            pyautogui.doubleClick(x, y)
            pyautogui.moveTo(10, 10)
            return True

    def find(self, template):
        """Find the given visual item on the screen, and return the percent position

        Arguments:
            item {Item} -- The visual item to be looked for on the screen

        Returns:
            tuple -- Tuple of the percent (x,y) position on the game frame 
            where the item was found. If the item wasn't found, return None
        """

        confidence = template.get_confidence()
        image_list = []
        if template.name in self.__template_cache:
            image_list = self.__template_cache[template.name]['image_list']
        else:
            self.__template_cache[template.name] = {}
            cache_obj = self.__template_cache[template.name]
            cache_obj['image_path_list'] = []
            for image, frame_size in template.image_list:
                h, w = image.shape[:2]
                cv2.resize(image, )
        for path in item.imglist:
            offset, screen = self.__itemcache.crop(screen, item)
            try:
                rect = pyautogui.locate(path, screen, confidence=confidence)
                if rect is None:
                    continue
                x = rect.left + rect.width/2 + offset[0]
                y = rect.top + rect.height/2 + offset[1]
                self.__itemcache.save(item, rect)
                return (x, y)
            except pyautogui.ImageNotFoundException:
                continue
        return None

    def find_all(self, item):
        all_list = []
        confidence = item.get_confidence()
        for i in item.imglist:
            try:
                #for pos in pyautogui.locateAll(i, screen, confidence=confidence):
                #    all_list.append(pos)
                pass
            except pyautogui.ImageNotFoundException:
                pass
        return all_list


def find_frame_vert(self, thresh):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, MIN_WINDOW_HEIGHT))
    vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) < 2:
        return None
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

    left_block = cv2.boundingRect(sorted_contours[0]) # (x, y, w, h)
    right_block = cv2.boundingRect(sorted_contours[1])
    if left_block[0] > right_block[0]: # Swap if left block is actually right block
        temp = left_block
        left_block = right_block
        right_block = temp

    if abs(left_block[1] - right_block[1]) > 3:
        return None
    if abs(left_block[3] - right_block[3]) > 3:
        return None
    
    x = left_block[0] + left_block[2]
    y = left_block[1]
    w = right_block[0] - x
    h = left_block[3]

    return (x, y, w, h)

def find_frame_hor(self, thresh):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (MIN_WINDOW_WIDTH, 1))
    horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) < 2:
        return None
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

    top_block = cv2.boundingRect(sorted_contours[0]) # (x, y, w, h)
    bottom_block = cv2.boundingRect(sorted_contours[1])
    if top_block[1] > bottom_block[1]: # Swap if left block is actually right block
        temp = top_block
        top_block = bottom_block
        bottom_block = temp

    if abs(top_block[0] - bottom_block[0]) > 3:
        return None
    if abs(top_block[2] - bottom_block[2]) > 3:
        return None
    
    x = top_block[0]
    y = top_block[1] + top_block[3]
    w = top_block[2]
    h = bottom_block[1] - y

    return (x, y, w, h)
