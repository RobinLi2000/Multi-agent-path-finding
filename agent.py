from base import (BaseAgent, action_dict, move,
                  set_timeout, after_timeout, TIMEOUT)


##################################################################################
# Here is a demo agent.                                                          #
# You can implement any helper functions.                                        #
# You must not remove the set_timeout restriction.                               #
# You can start your code any where but only the get_action() will be evaluated. #
##################################################################################


class MyAgent(BaseAgent):

    def get_avai_actions(self, game_state):
        avai_actions = []
        for action in action_dict:
            fake_action_profile = dict()
            for name in game_state:
                if name == self.name:
                    fake_action_profile[name] = action
                else:
                    fake_action_profile[name] = 'nil'
            succ_state = self.env.transition(game_state, fake_action_profile)
            if succ_state:
                avai_actions.append(action)
        return avai_actions
    '''last_position这个数组是用来记录上一个机器人下一步的位置'''
    @set_timeout(TIMEOUT, after_timeout)
    def get_action(self, game_state,last_position):
        #last_position=[]
        # Step 1. figure out what is accessible
        #print('last_position len:'+str(last_position))
        obs = self.observe(game_state)
        #print('game_state:'+str(game_state))
        #print('obs:'+str(obs))
        #print(str(obs[0:]))
        avai_actions = self.get_avai_actions(game_state)
        #print('action:'+str(avai_actions))
        goal = self.env.get_goals()[self.name]

        # Step 2. production system or any rule-based system
        min_dist = 999999
        best_action = None
        for action in avai_actions:
            succ = move(obs[0], action)
            #print('action is' +str(action))
            if succ in obs[1:] or succ in last_position or (succ in self.visited and action !='nil'):
                #print(str(action)+'action pass whether its colision or visited' )
                continue
            else:
                # 当机器人远离目标时，不要考虑保持静止这个动作。这个是为了解决机器人通向目标点最近的方向被另一个机器人挡住的时候，选择一
                # 条更远的路，因此在机器人接近目标点的时候，可以考虑让机器人静止在原地

                if (abs(goal[0] - obs[0][0]) + abs(goal[1] - obs[0][1])) >3 and action == 'nil':
                    # skip stay still
                    #print(str(action)+'action pass when it;s nil and far away goal' )
                    continue
                #其他时候不考虑静止动作，因为机器人有可能绕不开障碍物，一直呆再原地，因为呆在原地的时候cost值最低
                else:
                
                    # 计算当前节点和后继节点之间的距离c
                    c = (obs[0][0] - succ[0]) ** 2 + (obs[0][1] - succ[1]) ** 2
                    # 计算后继节点和目标点之间的启发距离h
                    h = (goal[0] - succ[0]) ** 2 + (goal[1] - succ[1]) ** 2 
                    #h = abs(goal[0] - succ[0]) + abs(goal[1] - succ[1])
                    # A*的cost等于c+h
                    dist = c+h
                    #print('action:'+str(action)+'cost'+str(dist))
                    
                    if dist <= min_dist:
                        min_dist = dist
                        best_action = action
        ''' 这里主要是把下一个节点的位置保存下来，用于下一个agent碰撞检测'''
        #首先清空last_position数组里面的节点
        last_position.clear()
        #计算best_action时的下一个节点的坐标
        succ_next = move(obs[0], best_action)
        #下一个节点的坐标如果不是目标点，加入visite数组，visite数组是为了防止机器人重复走之前走过的节点，造成死循环
        if succ_next != goal:
            self.visited.append(succ_next)
        # 把下一个节点的坐标加进visited数组中，并返回此机器人下一步的位置，让下一个机器人在规划时避开这个位置
        last_position.append(succ_next)
        print('best_action'+str(best_action)+'succ_next' + str(succ_next))
        return (best_action,last_position)
    

