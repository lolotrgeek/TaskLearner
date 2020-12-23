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
# https://stable-baselines.readthedocs.io/en/master/modules/dqn.html#example

profiler = Profiler()
profiler.start()

# Setup Environment
env = gym.make('Desktop-v0')
outdir = '/tmp/random-agent-results'
env = Monitor(env, directory=outdir, force=True)
episodes = 10
steplimit = 100
debug = True
noShow = True

# Setup Agent
model = DQN(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=10000, log_interval=4)
model.save("deepq_desktop")

del model # remove to demonstrate saving and loading

model = DQN.load("deepq_desktop")

if __name__ == '__main__':
    # Run Environment
    for episode in range(episodes):
        state = env.reset(steplimit=steplimit, debug=debug, noShow=noShow)
        reward = 0
        done = False
        print('Episode:' , episode)
        while True:
            if done is True:
                break
            action, _states = model.predict(state, deterministic=True)
            next_state, reward, done, _ = env.step(action)
            env.render()
            state = next_state
        print('Reward:', reward)
    # Stop Environment
    env.close()
    profiler.stop()

print(profiler.output_text(unicode=True, color=True))