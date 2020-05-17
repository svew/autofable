import pyautogui
import time
from constants import *
from config import *
from PIL import Image
from cv2 import cv2
import numpy as np
from item import *

# Current game state
game_frame = None
game_map = []
game_state = None
game_final_battle = False

#Start outside of battle
def main():
    global game_frame, game_state, game_final_battle

    print('\nSetting up bot, searching for game frame...')

    while game_frame is None:
        find_game_frame(pyautogui.screenshot())
        if game_frame is None:
            time.sleep(3)
    print('Found game frame')

    print('Waiting for the player to start outside the camp...')
    while True:
        screen = get_screenshot()
        if find_item(screen, START) is not None:
            break
        time.sleep(1)

    print('Starting bot')
    game_state = State.BEGIN
    time.sleep(1)
    click_direction(CENTER)
    
    while True:
        next_state = bot_loop(game_state)
        if next_state is not None:
            game_state = next_state

def bot_loop(state):
    global game_final_battle, game_map

    screen = get_screenshot()

    if state == State.BEGIN:
        print('Player inside camp, starting...')
        game_map = []
        game_map.append(RIGHT)
        game_map.append(RIGHT['flip']['next'])
        click_direction(RIGHT)
        time.sleep(1.5)
        return State.TRAVERSE

    if state == State.TRAVERSE:
        if press_button(screen, BANDIT_WAITING):
            print('Found a bandit, attacking!')
            return State.APPROACHING
        if press_button(screen, TENT):
            print('Found bandit tent, attacking!')
            game_final_battle = True
            return State.APPROACHING
        if find_item(screen, NOT_PAUSED) is None: # Game is paused, likely levelup
            print('Leveling up!')
            press_button(screen, LEVELUP)
            time.sleep(0.1)
            return
        # Nothing in this space, try traversing
        if game_map[-1]['flip'] == game_map[-2]: # Next move is back up the tree
            print(f'Backtracking in direction {game_map[-1]["name"]}')
            click_direction(game_map[-1])
            game_map[-2] = game_map[-2]['next']
            game_map.pop()
            time.sleep(2)
            return
        else:
            if is_path_clear(game_map[-1]):
                print(f'Path in direction {game_map[-1]["name"]}, traversing')
                click_direction(game_map[-1])
                game_map.append(game_map[-1]['flip']['next'])
                time.sleep(2)
                return
            else:
                print(f'No path found in direction {game_map[-1]["name"]}')
                game_map[-1] = game_map[-1]['next']
                return

    if state == State.APPROACHING:
        if find_item(screen, BATTLE):
            print('In battle!')
            return State.BATTLE
        else:
            time.sleep(0.2)
            return

    if state == State.BATTLE:
        if find_item(screen, MULTI):
            enemies = find_all_items(screen, BANDIT_BATTLE)
            print(f'I see {len(enemies)} enemies')
            if len(enemies) > 1:
                print('Throwing knives')
                press_button(screen, MULTI, sleep=2)
                return
            else:
                print('Attacking')
                press_button(screen, ATTACK, sleep=2)
                return
        elif press_button(screen, ATTACK):
            print('Attacking')
            time.sleep(2)
            return
        elif press_button(screen, OK): # Battle finished
            print('Battle over!')
            time.sleep(0.2)
            if game_final_battle:
                game_final_battle = False
                return State.AFTER_QUEST
            else:
                return State.TRAVERSE

    if state == State.AFTER_QUEST:
        if find_item(screen, NOT_PAUSED) is None: # Game is paused, likely levelup
            print('Leveling up!')
            if press_button(screen, LEVELUP):
                time.sleep(0.1)
                return
        if press_button(screen, CLOSE): # Collect Exp and Gold
            print('Collecting gold')
            time.sleep(0.5)
            return
        elif find_item(screen, KEEP): # New item!
            print('New item!')
            if KEEP_REWARD:
                print("I'll take it!")
                press_button(screen, KEEP, sleep=0.4)
                return
            else:
                print("I'll pass...")
                press_button(screen, PASS, sleep=0.3)
                press_button(screen, YES, sleep=0.3)
                return
        elif find_item(screen, START): #Outside camp, go get healed
            print('Getting healed...')
            click_direction(DOWN, sleep=1.5)
            click_direction(LEFT, sleep=2)
            click_direction(CENTER, sleep=1.5)
            press_button(None, TALK, sleep=0.3)
            press_button(None, HEAL, sleep=0.3)
            press_button(None, DONE, sleep=0.3)
            click_direction(RIGHT, sleep=2)
            click_direction(UP, sleep=2)
            return State.BEGIN


def get_screenshot():
    screen = pyautogui.screenshot()
    if game_frame is not None:
        screen.crop((game_frame[0], game_frame[1], game_frame[0] + game_frame[2], game_frame[1] + game_frame[3]))
    return screen

def click_direction(direction, sleep=0):
    if is_direction_invalid(direction):
        print(f'Provided direction invalid: {direction}')
    if game_frame is None:
        raise 'game_frame is null when asking to click direction'
    x = int(game_frame[0] + game_frame[2] * direction['x'])
    y = int(game_frame[1] + game_frame[3] * direction['y'])
    pyautogui.doubleClick(x, y)
    pyautogui.moveTo(10, 10)
    time.sleep(sleep)

def is_path_clear(direction):
    if is_direction_invalid(direction):
        print(f'Provided direction invalid: {direction}')
    x = int(game_frame[0] + game_frame[2] * direction['x'])
    y = int(game_frame[1] + game_frame[3] * direction['y'])
    pixel = pyautogui.pixel(x, y)
    print(f'Pixel: {pixel}')
    return pixel[1] > pixel[0] and pixel[1] > pixel[2]

def press_button(screen, button, sleep=0):
    if screen is None:
        screen = get_screenshot()
    pos = find_item(screen, button)
    if pos is None:
        return False
    else:
        x, y = pos
        pyautogui.doubleClick(x, y)
        pyautogui.moveTo(10, 10)
        time.sleep(sleep)
        return True

itemcache = ItemCache()
def find_item(screen, item):
    screen = screen or get_screenshot()
    confidence = item.get_confidence()
    for path in item.imglist:
        offset, screen = itemcache.crop(screen, item)
        try:
            rect = pyautogui.locate(path, screen, confidence=confidence)
            if rect is None:
                continue
            x = rect.left + rect.width/2 + offset[0]
            y = rect.top + rect.height/2 + offset[1]
            itemcache.save(item, rect)
            return (x, y)
        except pyautogui.ImageNotFoundException:
            continue
    return None

def find_all_items(screen, item):
    all_list = []
    confidence = item.get_confidence()
    for i in item.imglist:
        try:
            for pos in pyautogui.locateAll(i, screen, confidence=confidence):
                all_list.append(pos)
        except pyautogui.ImageNotFoundException:
            pass
    return all_list

def center(rect):
    return (rect[0] + rect[2]/2, rect[1] + rect[3]/2)

def find_game_frame(screen):
    global game_frame

    img = np.array(screen)
    thresh = cv2.inRange(img, WINDOW_BORDER_COLOR, WINDOW_BORDER_COLOR)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return

    window_border = max(contours, key=cv2.contourArea)
    x0, y0, w, h = cv2.boundingRect(window_border)
    window_crop = thresh[y0:y0+h, x0:x0+w]
    window_thresh = cv2.bitwise_not(window_crop)
    contours, _ = cv2.findContours(window_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return

    game_border = max(contours, key=cv2.contourArea)
    x1, y1, w, h = cv2.boundingRect(game_border)
    if w * h < 540*405:
        return

    game_frame = (x0 + x1, y0 + y1, w, h)

def is_direction_invalid(direction):
    if direction is None:
        return True
    if type(direction) is not dict:
        return True
    if 'x' not in direction or 'y' not in direction:
        return True
    return False