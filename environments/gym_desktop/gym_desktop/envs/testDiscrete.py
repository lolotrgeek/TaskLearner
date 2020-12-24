import gym_desktop.envs.actions as actions
from time import sleep

sent = []
action_space = actions.actionMap.actions

for action in action_space:
    print(str(action))
    if isinstance(action_space[action], list):
        # integers which represent key presses
        actions.main.key_stroke(action_space[action])
        sent.append([action, 'key'])

    elif isinstance(action_space[action], int):
        # list which represent x,y coordinate with a buttonmask (clicks)
        if action < 513:
            actions.main.mouse_action([0, action, 0, 0])  # delta_x
            sent.append([action, 'deltax'])
        elif action > 513 and action < 1025:
            actions.main.mouse_action([0, 0, action, 0])  # delta_y
            sent.append([action, 'deltay'])
        elif action == 1025:
            actions.main.mouse_action([action, 0, 0, 0])  # btn_1
            sent.append([action, 'btn1'])
        elif action == 1026:
            actions.main.mouse_action([action, 0, 0, 0])  # btn_2
            sent.append([action, 'btn2'])
        elif action == 1027:
            actions.main.mouse_action([action, 0, 0, 0])  # btn_3
            sent.append([action, 'btn3'])
        elif action == 1028:
            actions.main.mouse_action([0, 0, 0, 0])  # none
            sent.append([action, 'none'])
        elif action == 1029:
            actions.main.mouse_action([0, 0, 0, action])  # whl_dwn
            sent.append([action, 'whl_dwn'])
        elif action == 1030:
            actions.main.mouse_action([0, 0, 0, action])  # whl_none
            sent.append([action, 'whl_none'])
        elif action == 1031:
            actions.main.mouse_action([0, 0, 0, action])  # whl_up
            sent.append([action, 'whl_up'])
    else:
        print('NullEvent')

    sleep(.5)

with open('actionsSent.txt', 'w') as filehandle:
    for action in actions:
        if isinstance(action, list):
            filehandle.writelines("%s\n" % action)