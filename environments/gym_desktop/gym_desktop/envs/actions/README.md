# gymKeyStrokes

Based on [piKeyStrokes](https://github.com/lolotrgeek/piKeyStrokes/tree/remote) remote branch.

This overrides the piKeyStrokes API with a gym friendly API.

## Install
[Install piKeyStrokes.](https://github.com/lolotrgeek/piKeyStrokes/tree/remote#install)

## Usage
`humanMap.py` is for encoding actions into human readable format

`machineMap.py` is for encoding actions into machine readable format

Actions are keypresses, each keypress can be combined with modifiers

## Action Encodings

| AI Action (integer)  |      Human (string)      |  Machine (buffer) |
|----------|:-------------:|------:|
| 0 |  "KEYCODE_A" | 0x04 |
| 1 |    "KEYCODE_B"  |   0x05 |
| 2 | "KEYCODE_C" |    0x06 |
|...|
