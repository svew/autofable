
from AutoFable import down, left, up, center, click, is_background, right, visible

# Best starting place is wherever you wind up after the quest is completed
def start():
    click('Tomix')
    click('Quests')
    click('Penitentiary')
    click('More', count=8)
    click('Quest!')
    while not is_background('FirstArea'):
        click()
    right(count=4)
    down()
    right(count=5)
    while not visible('Complete'):
        click()

# If the player starts in the middle of Falconreach, how to navigate to the starting point
def from_falconreach():
    down()
    left()
    left()
    up()
    center()
    click('Use Portal')
