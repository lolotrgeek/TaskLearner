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
- actor: a raspberry pi with OTG (4/zero)
- client: a machine that accepts keyboard/mouse via usb
- agent: a machine that runs agent and sends actions to raspberry pi 
- a usb-hdmi video capture card
- optional: USB split power cable, is required if there are power issues

### Install on the agent
1. plug in hdmi video capture card
2. setup software environment with the following commands:
```
$ pip install gym opencv-python numpy pyinstrument imutils screeninfo pynput torch stable-baselines3 
$ pip install -e ./environments/gym_desktop 
```
or

```
$ conda activate tracker
```

### Install on the actor
1. Follow install instructions here: [piKeyStrokes](https://github.com/lolotrgeek/piKeyStrokes/tree/remote)
2. run an instance of piKeyStrokes

### Install on client
1. plug usb from raspberry pi OTG port to a usb on client
2. plug hdmi from client into hdmi capture card on agent

## Usage
Pick an agent from `/agents`

Example:
```
python agents/random_agent.py
```
Currently, the system is setup to send actions to a remote server. Without a server the actions will not register. Local actions are implemented, but needs a better way to toggle.

### To run remotely
 First install then start an instance of [piKeyStrokes](https://github.com/lolotrgeek/piKeyStrokes/tree/remote) on an OTG device. Connect the OTG device via usb to any system that has a gui and accepts keyboard/mouse inputs.

 Then run the above agent command.


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
