from constants import CacheType

# Settings
KEEP_REWARD = False
DEFAULT_CONFIDENCE = 0.9

# On-screen buttons/context markers
ATTACK = { 
    'img': ['images/attack.png'], 
    'cache': CacheType.SINGLE
}
BANDIT_WAITING = {
    'img': ['images/bandit_waiting_0.png', 'images/bandit_waiting_1.png'], 
    'cache': CacheType.NONE 
}
BANDIT_BATTLE = {
    'img': ['images/bandit_battle_0.png'],
    'cache': CacheType.NONE
}
TENT = {
    'img': ['images/tent.png'],
    'cache': CacheType.NONE
}
START = {
    'img': ['images/start.png'],
    'cache': CacheType.SINGLE
}
OK = { 
    'img': ['images/ok.png'],     
    'cache': CacheType.SINGLE 
}
MULTI =  { 
    'img': ['images/multi.png'],
    'cache': CacheType.SINGLE
}
BATTLE = {
    'img': ['images/inbattle.png'],
    'cache': CacheType.SINGLE
}
BOTTOM_LEFT = {
    'img': ['images/bottom_left.png'],
    'cache': CacheType.NONE
}
BOTTOM_RIGHT = {
    'img': ['images/bottom_right.png'],
    'cache': CacheType.NONE
}
CLOSE = {
    'img': ['images/close.png'],
    'cache': CacheType.SINGLE
}
KEEP = {
    'img': ['images/keep.png'],
    'cache': CacheType.SINGLE
}
PASS = {
    'img': ['images/pass.png'],
    'cache': CacheType.SINGLE
}
TALK = {
    'img': ['images/talk.png'],
    'cache': CacheType.SINGLE
}
HEAL = {
    'img': ['images/heal.png'],
    'cache': CacheType.SINGLE
}
DONE = {
    'img': ['images/done.png'],
    'cache': CacheType.SINGLE
}
YES = {
    'img': ['images/yes.png'],
    'cache': CacheType.SINGLE
}