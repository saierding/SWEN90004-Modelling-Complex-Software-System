# ========================================
# DEFINING STATIC PARAMS
# ========================================
# @date created: 20 May 2020
# @authors: Victor
# The file is used for defining the static params.

from dynamic_params import Dynamic_Params, INITIAL_COP_DENSITYS, INITIAL_AGENT_DENSITYS, VISIONS


K: float = 2.3                                                      # Factor for determining arrest probability
MAP_HEIGHT: int = 40                                                # Height of the patch map
MAP_WIDTH: int = 40                                                 # Width of the patch map
MAX_FRAMES = 1000                                                   # The number of frames to be ticked
REBELLION_THRESHOLD = 0.1                                           # The distance between G and N to make someone rebel


dynamic_params_filename = 'dynamic_params.json'
param_reader = Dynamic_Params(dynamic_params_filename).read_params(dynamic_params_filename)
VISION = param_reader[VISIONS[0]]                                   # Defines the radius of neighbourhood for any patch
INITIAL_COP_DENSITY = param_reader[INITIAL_COP_DENSITYS[0]]         # Percentage of cops
INITIAL_AGENT_DENSITY = param_reader[INITIAL_AGENT_DENSITYS[0]]     # Percentage of agents


def total_patches() -> int:
    """Total number of patches."""
    return MAP_HEIGHT * MAP_WIDTH


def total_cops() -> int:
    """Total number of cops."""
    return int(total_patches() * INITIAL_COP_DENSITY)


def total_agents() -> int:
    """Total number of agents."""
    return int(total_patches() * INITIAL_AGENT_DENSITY)

