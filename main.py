from src.fablescreen import FableScreen

def get_game_frame_size():
    screen = FableScreen()

    if screen.initialize() is False:
        print('Make the DragonFable game visible, and large enough to be detected.')
        print('Be sure to resize the window such that a red border appears on the side of the game')

        

if __name__ == '__main__':
    autofable.main()