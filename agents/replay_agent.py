import gym
import cv2
from gym.wrappers import Monitor
import gym_desktop
import time
import pickle

env = gym.make('Desktop-v0')
max_ep = 10
actions = []

class PointerEvent():
    def __init__(self, x=0, y=0, buttonmask=0, v_wheel=0, h_wheel=0):
        self.x = x
        self.y = y
        self.buttonmask = buttonmask
        self.v_wheel = v_wheel
        self.h_wheel = h_wheel

with open('listfile.data', 'rb') as filehandle:
    actions = pickle.load(filehandle)

# Run Environment
step_cnt = 0
ep_reward = 0
done = False
state = env.reset()

while not done:
    if step_cnt > len(actions):
        done = True
        break
    next_state, reward, done, _ = env.step([actions[step_cnt]])
    env.render()
    step_cnt += 1
    ep_reward += reward
    state = next_state
    # Press "q" to quit
    if cv2.waitKey(25) & 0xFF == ord("q"):
        env.close()
        break

print('Episode: {}, Step count: {}, Episode reward: {}'.format(
    1, step_cnt, ep_reward))

# Stop Environment
env.close()