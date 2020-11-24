import gym
from gym import error, spaces, utils
from gym.utils import seeding
import time
import cv2
import mss
import numpy as np

STATE_W = 800
STATE_H = 640


class DesktopEnv(gym.Env):
    """
    Description:
      A Desktop GUI is rendered and the agent is given a task to complete. The agent submits states
      it believes to solve the task to a validation function. The validation function returns a boolean,
      true when the task is complete.

    Source:


    Observation:
      Type: Box(n)
      Size of window


    Actions:
      Type: Discrete(126)
      String   Action
      0x01     hex keycode
      ...

    Rewards:
      action  .01
      statechange  delta(currentstate, laststate) ...with decay?
      failure = -.01
      [energyuse]


    Starting State:
      reload chromium at fullscreen
      center mouse
      release all keys

    Episode Termination:
      reward = -100
      Episode length is greater than 200 seconds.


    Solved Requirements:
      Considered solved when the given state returns true when passes to the validation function.
    """

    metadata = {'render.modes': ['human', "rgb_array", "state_pixels"]}

    # "rgb_array" returns "numpy.ndarray"
    # show image in same window like a video
    # https://stackoverflow.com/questions/59201850/how-can-i-show-an-image-in-the-same-frame-of-a-video-in-opencv-python

    def __init__(self):
        self.sct = mss.mss()
        self.start_time = time.time()
        self.time_limit = 10
        self.action_space = spaces.Discrete(140)

        self.observation_space = spaces.Box(
            low=0, high=255, shape=(STATE_H, STATE_W, 3), dtype=np.uint8
        )

    def step(self, action=None):
        self.last_time = time.time()
        self.state = np.array(self.sct.grab(
            {"top": 0, "left": 0, "width": STATE_W, "height": STATE_H}))
        done = False
        step_reward = 1
        if self.last_time - self.start_time > self.time_limit:
            done = True
        return self.state, step_reward, done, {}

    def reset(self):
        self.state = np.array(self.sct.grab(
            {"top": 0, "left": 0, "width": STATE_W, "height": STATE_H}))
        return self.state

    def render(self, mode='human'):
        if self.state is None:
            return None
        # print("fps: {}".format(1 / (time.time() - self.last_time)))
        return cv2.imshow("OpenCV/Numpy normal", self.state)

    def close(self):
        cv2.destroyAllWindows()
