import signal

import numpy as np

action_dict = {
    'nil': [0, 0],
    'up': [-1, 0],
    'right': [0, 1],
    'down': [1, 0],
    'left': [0, -1],
}


def move(curr, action):
    succ = tuple(np.add(curr, action_dict[action]))
    return succ


class BaseAgent():

    def __init__(self, name, env):
        self.name = name
        self.avai_action = []
        self.env = env
        self.last_position = []
        #加入visted数组，visite数组用来记录机器人之前走过的点，是为了防止机器人重复走之前走过的节点，造成死循环 
        self.visited = []

    def observe(self, game_state):
        me, others = game_state[self.name], []
        for name in game_state:
            if name == self.name:
                continue
            else:
                a = game_state[name]
                others.append(a)
        return tuple([me] + others)

    def get_action(self, game_state):
        pass


######################################
# You do not have read the following #
######################################


TIMEOUT = 1


def set_timeout(num, callback):
    def wrap(func):
        def handle(signum, frame):
            raise RuntimeError

        def to_do(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handle)
                signal.alarm(num)
                r = func(*args, **kwargs)
                signal.alarm(0)
                return r
            except RuntimeError:
                callback()
        return to_do

    return wrap


def after_timeout():
    raise RuntimeError("Time out!")
