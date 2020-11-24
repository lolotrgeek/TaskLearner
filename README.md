# Task Learner
Using Reinforcement Learning to achieve tasks in the digital world.

```
conda activate tracker
```

## Environment
### State
Screen captured as pixels.

### Actions
- Discrete
    -  All non-modifier keys
    - Each key has one action, "strike" which presses and releases the key
- Multi-Discrete
    - each key/button has two actions, "press" and "release"
    - modifier keys
    ```
        "enter",
        "backspace",
        "delete",
        "enter",
        "tab",
        "up",
        "down",
        "right",
        "left",
        "home",
        "end",
        "page_up",
        "page_down",
        "cmd",
        "alt_l",
        "ctrl_l",
        "shift",
        "space",
        "esc"
    ```
    - mouse buttons
    ```
    left, right, middle
    ```
    

- Continuous
    - mouse movements
    - mouse scroll

## Todo
- action space mouse mapping
- setup/test action space
- ship with conda env
- put gym_desktop into separate repo