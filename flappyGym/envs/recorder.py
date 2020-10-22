"""
The expert recorder.
"""
import argparse
import getch
import random
import gym
import numpy as np
import time
import os
import flappyGym.envs.Flappy
import time
import pygame
from pygame.locals import *

BINDINGS = {
    'a': 0,
    'd': 2}
SHARD_SIZE = 2000

def get_options():
    parser = argparse.ArgumentParser(description='Records an expert..')
    parser.add_argument('data_directory', type=str,
        help="The main datastore for this particular expert.")

    args = parser.parse_args()

    return args

FPS = 30
def run_recorder():
    """
    Runs the main recorder by binding certain discrete actions to keys.
    """
    ddir = "data"

    record_history = [] # The state action history buffer.

    env = gym.make('FlappyBird-v0')
    env._max_episode_steps = 1200

    ##############
    # BIND KEYS  #
    ##############

    action = None
    esc = False


    shard_suffix = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
    sarsa_pairs = []

    print("Welcome to the expert recorder")
    print("To record press either a or d to move the agent left or right.")
    print("Once you're finished press + to save the data.")
    print("NOTE: Make sure you've selected the console window in order for the application to receive your input.")

    while not esc:

        done = False
        _last_obs = env.reset()
        while not done and not esc:
            env.render()
            # Handle the toggling of different application states
            action = 0 
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_UP:
                    action = 1
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    esc = True
    
            obs, reward, done, info = env.step(action)
            time.sleep(1./FPS)
            sarsa = (_last_obs, action)
            _last_obs = obs
            sarsa_pairs.append(sarsa)

        if esc:
            env.close()
            break



    print("SAVING")
    # Save out recording data.
    num_shards = int(np.ceil(len(sarsa_pairs)/SHARD_SIZE))
    for shard_iter in range(num_shards):
        shard = sarsa_pairs[
            shard_iter*SHARD_SIZE: min(
                (shard_iter+1)*SHARD_SIZE, len(sarsa_pairs))]

        shard_name = "{}_{}.npy".format(str(shard_iter), shard_suffix)
        if not os.path.exists(ddir):
            os.makedirs(ddir)
        with open(os.path.join(ddir, shard_name), 'wb') as f:
            np.save(f, sarsa_pairs)

if __name__ == "__main__":
    run_recorder()
