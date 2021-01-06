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
$ pip install gym opencv-python numpy pyinstrument imutils screeninfo pynput torch stable-baselines3 
$ pip install -e ./environments/gym_desktop 
```
or

```
$ conda activate tracker
```

## Usage
Pick an agent from `/agents`
```
python agents/random_agent.py
```
Currently, the system is setup to send actions to a remote server. Without a server the actions will not register. Local actions are implemented, but needs a better way to toggle.

### To run remotely
 First install then start an instance of [piKeyStrokes](https://github.com/lolotrgeek/piKeyStrokes/tree/remote) on an OTG device. Connect the OTG device via usb to any system that has a gui and accepts keyboard/mouse inputs.

 Then run the above agent command.

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
- better connection checking
- local actions
- remote/local toggle
- custom rewards
- ship with conda env
- put environments into separate repos
