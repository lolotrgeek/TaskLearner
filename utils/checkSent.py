import pickle
# Decode binary of sent actions
actions = []
with open('listfile.data', 'rb') as filehandle:
    actions = pickle.load(filehandle)

# for action in actions:
#     print(action)


with open('actionsSent.txt', 'w') as filehandle:
    for action in actions:
        if isinstance(action, list):
            filehandle.writelines("%s\n" % action)