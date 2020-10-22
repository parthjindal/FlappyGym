import gym
import flappyGym.envs.Flappy
import time
import pygame

env=gym.make('FlappyBird-v0')
env.reset()  
FPS = 30
from pygame.locals import *
while True:
    action = 0 
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_UP:
            action = 1
    observation,reward,done,info=env.step(action)
    print(observation,reward)
    time.sleep(1./FPS)
    if(done):
        break
env.close()