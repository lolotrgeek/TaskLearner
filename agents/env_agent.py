

class Mod:
    def __init__(self, on, cost):
        self.on = False
        self.cost = 0    
    

class Output(Mod):
    def __init__(self, on, cost):
        super().__init__(on, cost)
        self.type = 'output'

    def act(self, action):
        pass

class Input(Mod):
    def __init__(self, on, cost):
        super().__init__(on, cost)
        self.type = 'input'

    def observe(self, inputs):
        return inputs

class Exchange(Output):
    def __init__(self, on=False, cost=1):
        super().__init__(on, cost)
        self.name = 'exchange'
    
    def act(self, action):
        print('doing exchange!', action)
        return


class Agent():
    def __init__(self, modules=[]):
        self.action_space = None
        self.state_space = None
        self.modules = modules
        pass

    def SetModule(self, module, action):
        '''
        Turn modules on or off, return cost
        '''
        cost = 0
        if action is not None:
            if module.name == action['module']:
                module.on = action['on']
                if module.on is True:
                    cost = module.cost    
            else: 
                print('module does not exist.')
        return cost

    def RunModule(self, module, action):
        '''
        Output modules and return observation for input module.
        '''


        return

    def step(self, actions):
        '''
        `action = { internal: [{ module: '', on: False | True }, ... ], external: [{module: '', action: 0}, ... ] }`
        '''
        reward = 0
        observation = []
        done = False 

        # Loop once to set state of all modules and eval internal reward
        for module in self.modules:
            for action in actions['internal']:
                cost = self.SetModule(module, action)
            reward = reward - cost

        # Loop again to run each module
        for module in self.modules:
            if module.on == True:
                if module.type == 'input':
                    observation.append(module.observe())
                
                elif module.type == 'output':
                    for action in actions['external']:
                        module.act(action['action'])
                else: 
                    print('Invalid Module type')
            else:
                print('Module is Off.')

        return observation, reward, done, {}

    def reset(self):
        pass
    def render(self):
        pass

# Test
agent = Agent(modules=[Exchange()])
actions = { 
    'internal': [{ 'module': 'exchange', 'on': True } ], 
    'external': [{'module': 'exchange', 'action': 0} ] 
}
observation, reward, done, _ = agent.step(actions)

print(observation, reward, done)