# Gym stuff
import gym
import gym_anytrading
from stable_baselines3 import PPO

# Stable baselines - rl stuff
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3 import A2C, PPO

# Processing libraries
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt



env = gym.make('stocks-v0')
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10_000)
vec_env = model.get_env()
obs = vec_env.reset()
for i in range(1000):
    action, _state = model.predict(obs, deterministic=True)
    obs, reward, done, info = vec_env.step(action)
    vec_env.render()
