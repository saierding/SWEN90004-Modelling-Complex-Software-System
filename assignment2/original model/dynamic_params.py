# ========================================
# DEFINING DYNAMIC PARAMS
# ========================================
# @date created: 20 May 2020
# @authors: Victor
# The file is used for defining the dynamic params.

import json


# Constants which provides default values for dynamic parameters
MAX_JAILED_TERM = ('max_jailed_term', 30)
GOVERNMENT_LEGITIMACY = ('government_legitimacy', 0.5)
MOVEMENT = ('movement', True)
FRAME_INTERVAL = ('frame_interval', 0.1)
INITIAL_COP_DENSITYS = ('initial_cop_density', 0.04)
INITIAL_AGENT_DENSITYS = ('initial_agent_density', 0.7)
VISIONS = ('vision', 7.0)

# Include all parameters here
DYNAMIC_PARAMETERS = [
    MAX_JAILED_TERM,
    GOVERNMENT_LEGITIMACY,
    MOVEMENT,
    FRAME_INTERVAL,
    INITIAL_COP_DENSITYS,
    INITIAL_AGENT_DENSITYS,
    VISIONS
]


class Dynamic_Params:

    def __init__(self, path):
        self.path = path

    # Read and return the params dict from the path
    def read_params(self, path) -> dict:
        with open(path, 'r') as file:
            params = json.load(file)
            return params

# s = Dynamic_Params('dynamic_params.json')
# print(s.read_params('dynamic_params.json'))
