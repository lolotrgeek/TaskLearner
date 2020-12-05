Relies on [pyKeyStrokes](https://github.com/lolotrgeek/piKeyStrokes)

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


## API
### press(key)
> key - type: `int`

> Press the given key

```
# write 'a'
press(1)
```

### pressModified(key)
> key - type: `int`

> Press the given key while holding SHIFT
```
# write '!'
pressModified(27)
```

### release()
releases all keys/modifiers