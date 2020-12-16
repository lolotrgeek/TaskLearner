import gym
import cv2
from gym.wrappers import Monitor
import gym_desktop
import time
import pickle

from pyinstrument import Profiler

profiler = Profiler()
profiler.start()

env = gym.make('Desktop-v0')
max_ep = 10
actions = []

with open('listfile.data', 'rb') as filehandle:
    actions = pickle.load(filehandle)

# Run Environment
step_cnt = 0
ep_reward = 0
done = False
state = env.reset(debug=False, noShow=False)

while not done:
    if step_cnt >= len(actions):
        done = True
        break
    next_state, reward, done, _ = env.step([actions[step_cnt]])
    env.render()
    step_cnt += 1
    ep_reward += reward
    state = next_state

print('Episode: {}, Step count: {}, Episode reward: {}'.format(
    1, step_cnt, ep_reward))

# Stop Environment
env.close()

profiler.stop()

print(profiler.output_text(unicode=True, color=True))