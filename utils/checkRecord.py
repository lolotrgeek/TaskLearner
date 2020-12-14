import pickle

actions = []
with open('listfile.data', 'rb') as filehandle:
    actions = pickle.load(filehandle)

# for action in actions:
#     print(action)


with open('actionsRecorded.txt', 'w') as filehandle:
    filehandle.writelines("%s\n" % action for action in actions)