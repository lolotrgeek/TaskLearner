import sys
from pyinstrument import Profiler

import gym
from gym.wrappers import Monitor
import gym_desktop

import numpy as np
from stable_baselines3 import DQN
from stable_baselines3.dqn import MlpPolicy

# Learn optimal policy with Q learning
# source: 
# https://stable-baselines3.readthedocs.io/en/master/modules/dqn.html

profiler = Profiler()
profiler.start()

# Setup Environment
env = gym.make('Desktop-v0', debug=True, show=True, steplimit=100)
outdir = '/tmp/random-agent-results'
env = Monitor(env, directory=outdir, force=True)
episodes = 10
# Setup Agent
model = DQN(MlpPolicy, env, verbose=0, buffer_size=100)
model.learn(total_timesteps=10000, log_interval=4)
model.save("deepq_desktop")

del model # remove to demonstrate saving and loading

model = DQN.load("deepq_desktop")

last_state = None
def unique_reward(state):
    # rewards a current state that is different from the last state
    return (np.sum(last_state) - np.sum(state))
    
# Run Environment
for episode in range(episodes):
    obs = env.reset()
    reward = 0
    done = False
    print('Episode:' , episode)
    while True:
        if done is True:
            break
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        last_state = obs
        env.render()
    print('Reward:', reward)
# Stop Environment
env.close()
profiler.stop()

print(profiler.output_text(unicode=True, color=True))