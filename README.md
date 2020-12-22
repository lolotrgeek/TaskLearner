# Task Learner
Using Reinforcement Learning to achieve tasks in the digital world.

## Goal
Create agents that...
- learn from raw pixels
- are indistinguishable from a human
- can be moved to different machines

## Setup

This setup uses a Raspberry Pi that consumes pixels from hdmi and sends mouse and keyboard events over usb.

What is needed:
- a raspberry pi with OTG (4/zero)
- a usb-hdmi video capture card
- optional: USB split power cable, is required if there are power issues

Install the following on the Pi
```
$ pip install gym opencv-python numpy pyinstrument imutils screeninfo
$ pip install -e ./environments/gym_desktop 
```
or

```
$ conda activate tracker
```



## Environment
### State
Screen captured as pixels.

### Actions
- Mouse
    - Move 2
    - Click 2
    - Scroll up 2 
    - Scroll down 2

- Keyboard
    - Standard keys: 61     
    - Modified keys: 61

- Special
    - Copy 2
    - Paste 2
    - Open 2

## Debugging
For state debugging run `agents/observer_agent.py`.

For action debugging create a record using `utils/record.py` and run `agents/replay_agent.py`.

## Todo
- ship with conda env
- put environments into separate repos
- refactor code
- rewards