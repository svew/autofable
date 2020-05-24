
class State:
    BEGIN = 0
    TRAVERSE = 1
    APPROACHING = 2
    BATTLE = 3
    AFTER_QUEST = 4

    
# Direction Markers
UP =     { 'x':0.50, 'y':0.01, 'flip':{}, 'next':{}, 'name':'Up' }
LEFT =   { 'x':0.01, 'y':0.50, 'flip':{}, 'next':{}, 'name':'Left' }
DOWN =   { 'x':0.50, 'y':0.81, 'flip':{}, 'next':{}, 'name':'Down' }
RIGHT =  { 'x':0.99, 'y':0.50, 'flip':{}, 'next':{}, 'name':'Right' }
CENTER = { 'x':0.50, 'y':0.40 }

UP['flip'] = DOWN
DOWN['flip'] = UP
LEFT['flip'] = RIGHT
RIGHT['flip'] = LEFT

UP['next'] = LEFT
LEFT['next'] = DOWN
DOWN['next'] = RIGHT
RIGHT['next'] = UP

DIRECTIONS = [UP, LEFT, DOWN, RIGHT]
