import gym
from gym import spaces
import numpy as np
from flappyGym.envs.utility import*

class FlappyEnv(gym.Env):
    '''
    Demo Environment to test OpenAI baselines

    '''
    def __init__(self):
        super().__init__()
        self.bird = Bird()
        lows=[0,-20,0,0]
        highs=[512,20,10,10]
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(low=np.array(lows),high=np.array(highs),dtype=np.float32)
        self.episode_step=0
    
    def step(self,action):
        self.episode_step +=1
        execute(action,self.bird)
        observation = self.observe()
        reward = self.calc_reward()
        done=False
        if(reward < 0):
            done=True
        return observation,reward,done,None

    def observe(self):
        return np.array([self.bird.playery, self.bird.playerVelY, self.bird.lowerPipes[0]['x']*0.01, self.bird.lowerPipes[0]['y']*0.01])
        
    def calc_reward(self):
        crashTest = checkCrash({'x': self.bird.playerx, 'y': self.bird.playery, 'index': 0},
                               self.bird.upperPipes, self.bird.lowerPipes)
        if crashTest[0] == True:
            return -10
        else:
            return 0.1

    def reset(self):
        initialize()
        movementinfo = showWelcomeAnimation(self.bird)
        mainGame(movementinfo,self.bird)
        self.episode_step=0
        return self.observe()

    def render(self, mode='human', close=False):
        pass
        