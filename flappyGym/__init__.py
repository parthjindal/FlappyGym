from gym.envs.registration import register

register(
        id='FlappyBird-v0',
        entry_point='flappyGym.envs:FlappyEnv',
        )