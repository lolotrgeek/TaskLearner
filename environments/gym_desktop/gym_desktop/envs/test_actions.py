import gym_desktop.envs.actions as actions
from time import sleep

sent = []
action_space = actions.actionMap.actions

for action in action_space:
    print(str(action))
    # Key Actions
    if isinstance(action_space[action], list):
        actions.main.key_stroke(action_space[action])
        sent.append([action, 'key'])
     # Mouse Actions
    elif isinstance(action_space[action], int):
        if action < 41:
            actions.main.mouse_action([0, action, 0, 0])  # delta_x
            sent.append([action, 'deltax'])
        elif action > 41 and action < 83:
            actions.main.mouse_action([0, 0, action, 0])  # delta_y
            sent.append([action, 'deltay'])
        elif action == 83:
            actions.main.mouse_action([action_space[action], 0, 0, 0])  # btn_1
            sent.append([action, 'btn1'])
        elif action == 84:
            actions.main.mouse_action([action_space[action], 0, 0, 0])  # btn_2
            sent.append([action, 'btn2'])
        elif action == 85:
            actions.main.mouse_action([action_space[action], 0, 0, 0])  # btn_3
            sent.append([action, 'btn3'])
        elif action == 86:
            actions.main.mouse_action([0, 0, 0, 0])  # none
            sent.append([action, 'none'])
        elif action == 87:
            actions.main.mouse_action([0, 0, 0, action_space[action]])  # whl_dwn
            sent.append([action, 'whl_dwn'])
        elif action == 88:
            actions.main.mouse_action([0, 0, 0, action_space[action]])  # whl_none
            sent.append([action, 'whl_none'])
        elif action == 89:
            actions.main.mouse_action([0, 0, 0, action_space[action]])  # whl_up
            sent.append([action, 'whl_up'])
    else:
        print('NullEvent')

with open('actionsSent.txt', 'w') as filehandle:
    for action in actions:
        if isinstance(action, list):
            filehandle.writelines("%s\n" % action)