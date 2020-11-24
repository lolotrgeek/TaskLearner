import time

import cv2
import mss
import numpy as np

import gym

# Mouse Support
# https://github.com/BoboTiG/python-mss/issues/55#issuecomment-580481146


class DesktopEnv():
# Part of the screen to capture
    def __init__(self):
        self.sct = mss.mss()


    def step(self, action=None):
        self.last_time = time.time()
        self.state = np.array(self.sct.grab({"top": 40, "left": 0, "width": 800, "height": 640}))
        done = False
        step_reward = 1

        return self.state, step_reward, done, {}

    def reset(self):
        pass

    def render(self, mode='human'):
        if self.state is None:
            return None
        print("fps: {}".format(1 / (time.time() - self.last_time)))
        return cv2.imshow("OpenCV/Numpy normal", self.state)

    def close(self):
        cv2.destroyAllWindows()


env = DesktopEnv()
while "Screen capturing":
    env.step()
    env.render()
    # Press "q" to quit
    if cv2.waitKey(25) & 0xFF == ord("q"):
        env.close()
        break
