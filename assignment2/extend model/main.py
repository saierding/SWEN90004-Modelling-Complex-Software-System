# ========================================
# DEFINING ENTRY POINT
# ========================================
# @date created: 20 May 2020
# @authors: Victor
# The file is used for defining the entry point of the project.

from time import sleep
from static_params import MAX_FRAMES
from map import World
from dynamic_params import Dynamic_Params, FRAME_INTERVAL


def main():

    init_frame = 1

    # Read dynamic parameters
    dynamic_params_filename = 'dynamic_params.json'
    param_reader = Dynamic_Params(dynamic_params_filename).read_params(dynamic_params_filename)

    # Initialise the world
    world = World(dynamic_params_reader=param_reader, out_filename='out.csv')

    while init_frame <= MAX_FRAMES:
        print('Frame #' + str(init_frame))
        world.update(init_frame)
        sleep(param_reader[FRAME_INTERVAL[0]])
        init_frame += 1


if __name__ == '__main__':
    main()