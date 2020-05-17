
from config import DEFAULT_CONFIDENCE

class CacheType:
    NONE = 0
    SINGLE = 1
    MULTI = 2

class Item:

    def __init__(self, name, imglist, cachetype=CacheType.NONE, confidence=None):
        self.name = name
        self.imglist = imglist
        self.cachetype = cachetype
        self.confidence = confidence

    def get_confidence(self):
        global DEFAULT_CONFIDENCE

        if self.confidence is None:
            return DEFAULT_CONFIDENCE
        return self.confidence

    def __str__(self):
        return self.name

class ItemCache:

    def __init__(self):
        self.cache = {}

    def crop(self, screen, item):
        if item.cachetype is CacheType.SINGLE and item in self.cache:
            cache_rect = self.cache[item]
            cropped = screen.crop(cache_rect)
            offset = (cache_rect[0], cache_rect[1])
            return offset, cropped
        return (0,0), screen

    def save(self, item, rect):
        if item.cachetype is CacheType.NONE:
            return
        if item.cachetype is CacheType.SINGLE:
            if item not in self.cache:
                self.cache[item] = self._to_pil_rect(rect)
                print(f'New cache for {item}: {self.cache[item]}')

    @staticmethod
    def _to_pil_rect(rect):
        return (rect.left, rect.top, rect.left + rect.width, rect.top + rect.height)


# On-screen buttons/context markers
ATTACK = Item(
    name='ATTACK',
    imglist=['images/attack.png'], 
    cachetype=CacheType.SINGLE)

BANDIT_WAITING = Item(
    name='BANDIT_WAITING',
    imglist=['images/bandit_waiting_0.png', 'images/bandit_waiting_1.png'])

BANDIT_BATTLE = Item(
    name='BANDIT_BATTLE',
    imglist=['images/bandit_battle_0.png'])

TENT = Item(
    name='TENT',
    imglist=['images/tent.png'])

START = Item(
    name='START',
    imglist=['images/start.png'],
    cachetype=CacheType.SINGLE)

OK = Item(
    name='OK',
    imglist=['images/ok.png'],     
    cachetype=CacheType.SINGLE)

MULTI = Item(
    name='MULTI',
    imglist=['images/multi.png'],
    cachetype=CacheType.SINGLE)

BATTLE = Item(
    name='BATTLE',
    imglist=['images/inbattle.png'],
    cachetype=CacheType.SINGLE)

CLOSE = Item(
    name='CLOSE',
    imglist=['images/close.png'],
    cachetype=CacheType.SINGLE)

KEEP = Item(
    name='KEEP',
    imglist=['images/keep.png'],
    cachetype=CacheType.SINGLE)

PASS = Item(
    name='PASS',
    imglist=['images/pass.png'],
    cachetype=CacheType.SINGLE)

TALK = Item(
    name='TALK',
    imglist=['images/talk.png'],
    cachetype=CacheType.SINGLE)

HEAL = Item(
    name='HEAL',
    imglist=['images/heal.png'],
    cachetype=CacheType.SINGLE)

DONE = Item(
    name='DONE',
    imglist=['images/done.png'],
    cachetype=CacheType.SINGLE)

YES = Item(
    name='YES',
    imglist=['images/yes.png'],
    cachetype=CacheType.SINGLE)

NOT_PAUSED = Item(
    name='NOT_PAUSED',
    imglist=['images/notpaused.png'],
    cachetype=CacheType.SINGLE)

LEVELUP = Item(
    name='LEVELUP',
    imglist=['images/levelup.png'],
    cachetype=CacheType.SINGLE)