import gym
from gym import error, spaces, utils
from gym.utils import seeding
import time
import cv2
import mss
import numpy as np
import faulthandler
import gym_desktop.envs.actions as actions
from gym_desktop.envs.events import KeyEvent, PointerEvent, WaitEvent

faulthandler.enable()

# State Constants
STATE_W = 800   
STATE_H = 640

# Action Constants
keyMap = actions.keymaps.machineKeyMap.keys

def keycode(key):
    if key in keyMap:
        return keyMap[key]
    else:
        raise error.Error(
            'Not sure how to translate to keycode: {!r}'.format(key))



class ActionSpace(gym.Space):
    """The space of Desktop actions.
    https://github.com/openai/universe/blob/master/universe/spaces/vnc_action_space.py

    You can submit a list of KeyEvents or PointerEvents. KeyEvents
    correspond to pressing or releasing a key. PointerEvents correspond
    to moving to a specific pixel, and setting the mouse buttons to some state
    (buttonmask is a bitmap corresponding to which buttons are down).

    Note that key releases work differently from click releases: keys
    are stateful and must be explicitly released, while the state of
    the mouse buttons is provided at each timestep, so you have to
    explicitly keep the mouse down.

    Attributes:
        keys (list<KeyEvent>): The allowed key presses
        buttonmasks (list<int>): The allowed buttonmasks (i.e. mouse presses)
        screen_shape (int, int): The X and Y dimensions of the screen

    """

    def __init__(self, keys=None, buttonmasks=None, screen_shape=(STATE_W, STATE_H)):
        # TODO : document & consider removing extra mapping?
        self.keys = []
        if keys is None:
            keys = keyMap
            print('load keymap')
        for key in keys:
            # print('setting keys')
            # keys[key]
            # down = KeyEvent.by_name(key, down=True)
            # up = vnc_event.KeyEvent.by_name(key, down=False)
            # self.keys.append(down)
            # self.keys.append(up)
            self.keys.append(key)
        self._key_set = set(self.keys)
        self._wait = 0
        self.screen_shape = screen_shape
        if self.screen_shape is not None:
            self.buttonmasks = []
            if buttonmasks is None:
                buttonmasks = range(256)
            for buttonmask in buttonmasks:
                self.buttonmasks.append(buttonmask)
            self._buttonmask_set = set(self.buttonmasks)

    def contains(self, action):
        if not isinstance(action, list):
            return False

        for a in action:
            if isinstance(a, KeyEvent):
                if a not in self._key_set:
                    return False
            elif isinstance(a, PointerEvent):
                if self.screen_shape is None:
                    return False

                if a.x < 0 or a.x > self.screen_shape[0]:
                    return False
                elif a.y < 0 or a.y > self.screen_shape[1]:
                    return False
                elif a.buttonmask not in self._buttonmask_set:
                    return False
            elif isinstance(a, WaitEvent):
                if a.amount < self._wait:
                    return False
        return True

    def sample(self):
        # Both key and pointer allowed
        if self.screen_shape is not None:
            event_type = self.np_random.randint(2)
        else:
            event_type = 0

        if event_type == 0:
            # Let's press a key
            key = self.np_random.choice(self.keys)
            event = [key]
        else:
            x = self.np_random.randint(self.screen_shape[0])
            y = self.np_random.randint(self.screen_shape[1])
            buttonmask = self.np_random.choice(self.buttonmasks)

            event = [PointerEvent(x, y, buttonmask)]
            # event = []
        return event


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
        self.no_show=False
        self.camera = cv2.VideoCapture(0)
        self.codec = 0x47504A4D  # MJPG
        # self.camera.set(cv2.CAP_PROP_FPS, 30.0)
        self.camera.set(cv2.CAP_PROP_FOURCC, self.codec)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, STATE_W)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, STATE_H)
        # self.sct = mss.mss()
        self.start_time = time.time()
        self.time_limit = 1000
        self.action_space = ActionSpace()
        self.observation_space = spaces.Box(
            low=0, high=255, shape=(STATE_H, STATE_W, 3), dtype=np.uint8
        )

    def step(self, action=None):
        err_msg = "%r (%s) invalid" % (action, type(action))
        assert self.action_space.contains(action), err_msg
        self.last_time = time.time()
        if not self.camera.isOpened():
            # capture local desktop if capture card is not present
            # self.state = np.array(self.sct.grab(
            #     {"top": 0, "left": 0, "width": STATE_W, "height": STATE_H}))
            self.state=np.array({})
        elif self.no_show is False:
            ret, im = self.camera.read(0)
            if not ret:
                print("failed to grab frame")
            self.state = im
        else:
            self.state=np.array({})    

        done = False
        step_reward = 1
        # Actions:
        for a in action:
            # print(str(a))
            if isinstance(a, dict):
                # TODO: move to next state but, wait x amount before taking next action...
                # time.sleep(a["wait"])
                return self.state, step_reward, done, {}
            elif isinstance(a, int):
                # integers which represent key presses
                actions.main.key_stroke(keyMap[a])
                # print(str(keyMap[a]))
                    
            elif isinstance(a, list):
                # list which represent x,y coordinate with a buttonmask (clicks)
                actions.main.mouse_action(a)
                # print(str(a[1]), ',', str(a[2]))

        if self.last_time - self.start_time > self.time_limit:
            print("Ending...")
            done = True
        return self.state, step_reward, done, {}

    def reset(self):
        # self.camera.release()
        actions.main.key_release()
        actions.main.mouse_action([0,0,0,0,0])
        cv2.destroyAllWindows()
        ret, im = self.camera.read(0)
        if self.no_show is False:
            self.state = im
        elif not ret:
            print("failed to grab frame")
            self.state = None
        else:
            self.state=np.array({})   
        # TODO: clear clipboard
        return self.state

    def render(self, mode='human'):
        if self.state is None:
            print('Unable to render.')
            return None
        try:
            print("fps: {}".format(1 / (time.time() - self.last_time)))
        except ZeroDivisionError:
            pass
        if self.no_show is False:
            cv2.imshow("OpenCV/Numpy normal", self.state)
            # https://raspberrypi.stackexchange.com/a/91144
            cv2.waitKey(1)
        return self.state

    def close(self):
        actions.main.key_release()
        self.camera.release()
        cv2.destroyAllWindows()
