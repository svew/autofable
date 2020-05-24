
import pyautogui
import numpy as np
import time
import os
from cv2 import cv2

from item import ItemCache

WINDOW_BORDER_COLOR = (0, 0, 102)
CAPTURE_FREQUENCY_MS = 100
GAME_FRAME_RATIO = 1.6666

GAME_VIEW_FEATURES_SIZE = (200, 333) # (height, width), resized image size for identifying features
GAME_VIEW_DETAILS_SIZE = (600, 1000) # (height, width), resized image size for identifying details

class FableScreen:

    def __init__(self):
        self.__frame = None # Most recent capture of the screen
        self.__frame_rect = None # Rect describing part of the screen where game exists. (top, left, width, height)
        self.__frame_capture_time = None # Time of the most recent capture of the screen
        self.__itemcache = ItemCache()

        self.size = None # Dimensions of the game screen

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
        height = img.shape[0]

        # Get an image only containing the very tall dark-red elements of the screen
        thresh = cv2.inRange(img, WINDOW_BORDER_COLOR, WINDOW_BORDER_COLOR)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, height//2))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        # Isolate the two largest dark-red blocks, incase there were additional blocks for some reason
        contours, _ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) < 2: # Should be two blocks, directly left and right of the screen
            return False
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
        left_block = cv2.boundingRect(sorted_contours[0]) # (x, y, w, h)
        right_block = cv2.boundingRect(sorted_contours[1])
        if left_block[0] > right_block[0]: # Swap if left block is actually right block
            temp = left_block
            left_block = right_block
            right_block = temp

        # Only allow a few pixels of y-pos/height disagreement between the blocks
        if abs(left_block[1] - right_block[1]) > 3:
            return False
        if abs(left_block[3] - right_block[3]) > 3:
            return False
        
        x = left_block[0] + left_block[2]
        y = left_block[1]
        w = right_block[0] - x
        h = left_block[3]

        self.__frame_rect = (x, y, w, h)
        self.size = (w, h)

        return True

    def is_in_battle(self):
        """Returns whether the player is currently engaged in battle.

        Returns:
            bool -- Whether the player is currently engaged in battle
        """
        return True

    def is_new_location(self, confidence=0.8):
        """Returns whether the player has moved to a different location. Location refers to the
        screen the character is on, not where the character exists on the screen.

        Keyword Arguments:
            confidence {float} -- Confidence threshold for determining if the screen changed. (default: {0.8})

        Returns:
            bool -- True if it's believed that the player has changed location. 'True' is only returned once per
                location change, so if the player moves location only a single time, repeated calls would return 'True'
                on the first call, then 'False' on further calls.
        """
        return False

    def is_game_view_active(self):
        """Returns whether the player's game view is active, meaning there are no pop-ups 
        """
        return True:

    def is_talking(self, bubble_size=0.03):
        """Returns whether the player is currently talking to an NPC, more accurately, if a white speech bubble is 
        detected.
        """
        game_view = self.__get_game_view()
        shrink = cv2.resize(game_view, GAME_VIEW_FEATURES_SIZE)
        ksize = (GAME_VIEW_FEATURES_SIZE[0] // 40) * 2 + 1
        median = cv2.medianBlur(game_view, ksize)
        

    def click_on(self, button, sleep=0):
        """Click on the button with the given button name if found on the screen

        Arguments:
            button {Item} -- The visual item to be looked for on the screen

        Keyword Arguments:
            sleep {float} -- How many seconds to sleep after a successful click (default: {0})

        Returns:
            bool -- True if the button was found and clicked on, False if otherwise
        """

        pos = self.find(button)
        if pos is None:
            return False
        else:
            x, y = pos
            pyautogui.doubleClick(x, y)
            pyautogui.moveTo(10, 10)
            time.sleep(sleep)
            return True

    def find(self, item):
        """Find the given visual item on the screen, and return the percent position

        Arguments:
            item {Item} -- The visual item to be looked for on the screen

        Returns:
            tuple -- Tuple of the percent (x,y) position on the game frame 
            where the item was found. If the item wasn't found, return None
        """

        confidence = item.get_confidence()
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

    def __get_frame(self):
        if self.__frame_rect is None:
            raise 'FableGame not initialized'
        if self.__frame_capture_time is not None:
            next_capture = self.__frame_capture_time + CAPTURE_FREQUENCY_MS
            if next_capture < time.time_ns() // 1000000:
                return self.__frame # We have a recent frame stored
        screen = pyautogui.screenshot()
        self.__frame_capture_time = time.time_ns() // 1000000
        rect = self.__frame_rect
        screen.crop((rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3]))
        self.__frame = screen

    def __get_game_view(self):
        frame = self.__get_frame()
        height = frame.shape[1] / GAME_FRAME_RATIO
        return frame[:height]

    def __get_game_bar(self):
        frame = self.__get_frame()
        y = frame.shape[1] / GAME_FRAME_RATIO
        return frame[y:]

