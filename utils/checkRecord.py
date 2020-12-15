import pickle

actions = []
with open('listfile.data', 'rb') as filehandle:
    actions = pickle.load(filehandle)

# for action in actions:
#     print(action)


with open('actionsRecorded.txt', 'w') as filehandle:
    for action in actions:
        if isinstance(action, list):
            filehandle.writelines("%s\n" % action)