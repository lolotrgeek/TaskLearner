import gym
import cv2
from gym.wrappers import Monitor
import gym_desktop



# Takes defined actions and observes the environment

env = gym.make('Desktop-v0')
max_ep = 10

class PointerEvent():
    def __init__(self, x=0, y=0, buttonmask=0, v_wheel=0, h_wheel=0):
        self.x = x
        self.y = y
        self.buttonmask = buttonmask
        self.v_wheel = v_wheel
        self.h_wheel =h_wheel

for ep_cnt in range(max_ep):
    step_cnt = 0
    ep_reward = 0
    done = False
    state = env.reset()

    while not done:
        next_state, reward, done, _ = env.step([1, PointerEvent(x=0, y=0, buttonmask=0 ), 123])
        env.render()
        step_cnt += 1
        ep_reward += reward
        state = next_state
        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            env.close()
            break
    print('Episode: {}, Step count: {}, Episode reward: {}'.format(ep_cnt, step_cnt, ep_reward))

env.close()