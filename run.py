import argparse
import os
import sys

import numpy as np

from agent import MyAgent
from animator import Animation
from game import Env, Game


def parse_map_from_file(map_config):
    PREFIX = 'maps/'
    POSTFIX = '.map'
    if not os.path.exists(PREFIX + map_config + POSTFIX):
        raise ValueError('Map config does not exist!')
    layout = []
    with open(PREFIX + map_config + POSTFIX, 'r') as f:
        line = f.readline()
        while line:
            if line.startswith('#'):
                pass
            else:
                row = []
                for char in line:
                    if char == '.':
                        row.append(0)
                    elif char == '@':
                        row.append(1)
                    else:
                        continue
                layout.append(row)
            line = f.readline()
    return np.array(layout)


def parse_goals(goals):
    goal_dict = dict()
    for i, goal in enumerate(goals):
        goal_dict[f'p{i + 1}'] = eval(goal.replace('_', ','))
    return goal_dict


def get_args():
    parser = argparse.ArgumentParser(
        description='Multi-Agent Path Finding Term Project.'
    )

    parser.add_argument('--agents', dest='agents', type=str, nargs='+',
                        help='Specify a list of agent names')
    parser.add_argument('--map', dest='map', type=str,
                        help='Specify a map')
    parser.add_argument('--goals', dest='goals', type=str, nargs='+',
                        help='Specify the goals for each agent,'
                             'e.g. 2_0 0_2')
    parser.add_argument('--vis', dest='vis', action='store_true',
                        help='Visulize the process')
    parser.add_argument('--save', dest='save', type=str,
                        help='Specify the path to save the animation vedio')
    parser.add_argument('--eval', dest='eval', action='store_true',
                        help='Do evaluation')

    args = parser.parse_args()

    map_name = args.map
    args.map = parse_map_from_file(args.map)

    args.goals = parse_goals(args.goals)
    
    #map_name = 'empty'
    #args.map = parse_map_from_file('empty')

    #args.goals = parse_goals('5_5 1_5')

    return args, map_name


def show_args(args):
    args = vars(args)
    for key in args:
        print(f'{key.upper()}:')
        print(args[key])
        print('-------------\n')


def get_starts(agents):
    starts = dict()
    for name in agents:
        char = input(f'Specify an initial position for agent {name}: ')
        if char.lower() == 'n':
            print('Program terminates')
            return None
        starts[name] = eval(char.replace(' ', ','))
    return starts


if __name__ == '__main__':
    args, map_name = get_args()

    if not args.eval:
        show_args(args)

        env = Env(args.goals, args.map, map_name)

        agents = []
        for name in args.agents:
            agents.append(MyAgent(name, env))

        starts = get_starts(args.agents)

        while starts:
            print('\nSTARTS:')
            print(starts)
            print('-------------\n')

            game = Game(starts, agents, env)
            history, score = game.run()
            print(f'==> Score: {score}\n')

            if args.vis:
                animator = Animation(args.agents,
                                     args.map,
                                     list(starts.values()),
                                     list(args.goals.values()),
                                     history)
                animator.show()
                if args.save:
                    animator.save(file_name=f'recording/{args.save}',
                                  speed=100)

            starts = get_starts(args.agents)

    else:
        stdout_fd = sys.stdout
        sys.stdout = open("eval.log", "w")

        NUM_ROUNDS = {
            'test': 20,
            'empty': 10,
            'small': 10,
            'medium': 20,
            'large': 30,
        }
        env = Env(args.goals, args.map, map_name)
        agents = []
        for name in args.agents:
            agents.append(MyAgent(name, env))

        num_rounds = NUM_ROUNDS[map_name]
        score_list = []
        i = 0
        while i < num_rounds:
            initials = np.random.choice(range(len(args.map)),
                                        size=(len(agents), 2),
                                        replace=False)
            # print(initials)
            invalid = False
            for pos in initials:
                # print(args.map[tuple(pos)])
                if args.map[tuple(pos)] == 1:
                    invalid = True
                    break
                if map_name == 'large' and pos[0] > 110 and pos[1] < 50:
                    break
            if invalid:
                continue

            starts = dict()
            for k in range(len(agents)):
                starts[agents[k].name] = tuple(initials[k])
            game = Game(starts, agents, env)
            history, score = game.run()
            score_list.append(score)
            i += 1

        sys.stdout = stdout_fd
        print(score_list)
        print(np.mean(score_list))
