# ========================================
# DEFINING MAP CLASS
# ========================================
# @date created: 20 May 2020
# @authors: Victor, jinxin, Fanlin
# The file is used for defining a world of agents, cops and patches.

from static_params import total_cops, total_agents, REBELLION_THRESHOLD, \
    K, VISION, MAP_WIDTH, MAP_HEIGHT, DANGEROUS_THRESHOLD
from dynamic_params import MAX_JAILED_TERM, MOVEMENT, GOVERNMENT_LEGITIMACY
from math import exp, floor, sqrt, pow
import random
import csv


class World:

    def __init__(self, dynamic_params_reader, out_filename):
        """
        Create all components.
        """
        self.params_reader = dynamic_params_reader
        self.out_filename = out_filename
        self.patch_map = PatchMap(self)
        self.turtles = []

        for i in range(total_cops()):
            self.turtles.append(Cop(self))

        for i in range(total_agents()):
            self.turtles.append(Agent(self))

        with open(out_filename, 'w') as out_file:
            csv_writer = csv.writer(out_file)
            # Extension: add 'killed' and replace 'quiet' to 'quiet_alive'
            header_columns = ['frame', 'quiet', 'quiet_alive', 'killed', 'jailed', 'active']
            csv_writer.writerow(header_columns)

    def update(self, frame):
        """
        Update all component in one frame.
        """
        random.shuffle(self.turtles)

        # update each turtle's patch
        for turtle in self.turtles:
            turtle.update()

        # update each status
        agents, quiet, jailed, active = [], [], [], []

        # Extension: add two attributes
        quiet_alive, killed = [], []

        for i in self.turtles:
            if isinstance(i, Agent):
                agents.append(i)
        for i in agents:
            if i.is_quiet():
                quiet.append(i)
        for i in agents:
            if i.is_jailed():
                jailed.append(i)
        for i in agents:
            if i.active:
                active.append(i)
        for i in quiet:
            if i.alive:
                quiet_alive.append(i)
            else:
                killed.append(i)

        # update new row in out_filename
        with open(self.out_filename, 'a') as out_file:
            csv_write = csv.writer(out_file)
            columns = [frame, len(quiet), len(quiet_alive), len(killed), len(jailed), len(active)]
            csv_write.writerow(columns)

    def get_dynamic_param(self, key):
        """Get the value of dynamic parameters"""
        return self.params_reader[key]


class Turtle:
    """
    simulates a turtle object, in which the behaviours are shared by both cop and turtle.
    """

    def __init__(self, world) -> None:
        """place itself to a patch."""
        self.world = world
        self.patch = None

    def movement(self) -> bool:
        """determines whether this turtle can move. by default it can always move."""
        return True

    def move(self, *args) -> None:
        """
        move to a random, unoccupied patch if it can move or
        they need to have an initial location).
        """

        if not self.movement():
            return

        if self.patch is not None:
            self.patch.remove_turtle(self)

        if len(args) == 0:
            new_patch = self.world.patch_map.get_random_unoccupied_patch(self.patch)

            # only move to the new patch if there is one available
            if new_patch is not None:
                self.patch = new_patch
                new_patch.add_turtle(self)

        if len(args) == 1:
            if args[0] is not None:
                self.patch = args[0]
                args[0].add_turtle(self)

    def update(self) -> None:
        """update the current state by moving to another place"""
        self.move()


class Cop(Turtle):
    """
    simulates a cop.
    """

    def update(self) -> None:
        """perform relevant action as a cop."""
        super().update()

        if self.patch is not None:
            self.enforce()

    def enforce(self) -> None:
        """
        find and arrest a random active agent in the neighbourhood.
        """

        # find all active agents in the neighbourhood
        agents = PatchMap.filter_neighbour_turtles(
            self.patch,
            lambda t: isinstance(t, Agent) and t.active
        )

        # don't continue if there is no matched agent
        if len(agents) == 0:
            return

        # move to the patch of the (about-to-be) jailed agent
        suspect = random.choice(agents)
        self.move(suspect.patch)

        # arrest suspect
        suspect.active = False

        # Extension: if suspect is dangerous, allocate a permanent jailed-term
        if suspect.is_dangerous():
            suspect.jail_term = -1
        else:
            if self.world.get_dynamic_param(MAX_JAILED_TERM[0]) == 0:
                suspect.jail_term = 0
            else:
                suspect.jail_term = random.randint(1, self.world.get_dynamic_param(MAX_JAILED_TERM[0]))


class Agent(Turtle):
    """
    simulates an agent object.
    """
    jail_term: int              # remaining time length for jailing
    active = bool               # indicates whether the turtle is open rebelling
    risk_aversion: float        # the degree of reluctance to take risks
    perceived_hardship: float   # perceived hardship of rebelling

    # Extension: add a new attribute that indicate whether the turtle is alive
    alive: bool

    def __init__(self, world) -> None:
        """ initialise the agent """
        super().__init__(world)
        self.jail_term = 0
        self.active = False
        self.risk_aversion = random.uniform(0, 1)
        self.perceived_hardship = random.uniform(0, 1)
        self.alive = True

    def update(self) -> None:
        """determines whether to open rebel."""

        # Extension: only alive agent can update
        if self.alive:
            super().update()

            # only determine behaviour if it is not jailed
            if self.patch is not None and not self.is_jailed():
                self.determine_behaviour()

                # Extension: dangerous agent can kill one quiet agent in the neighbourhood
                self.kill_quiet_agent()

            # reduce jail term
            self.decrement_jail_term()

    def movement(self) -> bool:
        """
        if it is jailed or movement is manually disabled it cannot move
        """
        return super().movement() and not self.is_jailed() and \
               self.world.get_dynamic_param(MOVEMENT[0]) is True

    def is_jailed(self) -> bool:
        """determine whether this agent is currently jailed."""

        # Extension: dangerous agent need to jailed forever
        return hasattr(self, 'jail_term') and (self.jail_term > 0 or self.jail_term == -1)

    def is_quiet(self) -> bool:
        """determine whether this patch is quiet (i.e. inactive & not jailed)."""
        return (not self.active) and (not self.is_jailed())

    def get_grievance(self) -> float:
        """calculate and return the grievance of the agent."""

        # Extension: make perceived_hardship of an agent can be influenced by the agents
        # in the neighbourhood
        active_agents_neighbour = PatchMap.filter_neighbour_turtles(
            self.patch,
            lambda t: isinstance(t, Agent) and t.active
        )
        total_active_agents = len(active_agents_neighbour)
        total_perceived_hardship = 0

        if total_active_agents > 0:
            for i in active_agents_neighbour:
                total_perceived_hardship += i.perceived_hardship

            average_perceived_hardship = total_perceived_hardship / total_active_agents
            return ((self.perceived_hardship + average_perceived_hardship) / 2) * \
                   (1 - self.world.get_dynamic_param(GOVERNMENT_LEGITIMACY[0]))
        else:
            return self.perceived_hardship * \
                   (1 - self.world.get_dynamic_param(GOVERNMENT_LEGITIMACY[0]))

    def get_estimated_arrest_probability(self) -> float:
        """calculate and return the estimated arrest probability of the agent
        (based on the formula)."""
        # c = number of neighbour cops
        c = len(PatchMap.filter_neighbour_turtles(self.patch, lambda t: isinstance(t, Cop)))

        # a = 1 + number of neighbour turtles which are active
        a = 1 + len(PatchMap.filter_neighbour_turtles(
            self.patch,
            lambda t: isinstance(t, Agent) and t.active
        ))

        return 1 - exp(-K * floor(c/a))

    def determine_behaviour(self) -> None:
        """determine the behaviour of this agent by flagging its activeness."""
        self.active = (self.get_grievance() - self.risk_aversion *
                       self.get_estimated_arrest_probability()) > REBELLION_THRESHOLD

    def decrement_jail_term(self) -> None:
        """ decrement the jail term by 1 if it is positive """
        if self.jail_term > 0:
            self.jail_term -= 1

    # Extension: determine if agent is dangerous or not
    def is_dangerous(self) -> bool:
        return self.perceived_hardship > DANGEROUS_THRESHOLD

    # Extension: dangerous agent can kill a quiet agent in the neighbourhood
    def kill_quiet_agent(self) -> None:
        if self.active and self.is_dangerous():
            # find all quiet agents in the neighbourhood
            agents = PatchMap.filter_neighbour_turtles(
                self.patch, lambda t: isinstance(t, Agent) and not t.active
            )
            if len(agents) == 0:
                return
            suspect = random.choice(agents)
            suspect.alive = False


class Patch:
    """
    Patch class
    """

    def __init__(self, x, y):
        """init function"""
        self.x = x
        self.y = y
        self.turtles = []
        self.neighbour_patches = []

    def add_turtle(self, turtle):
        """add turtle function"""
        self.turtles.append(turtle)

    def remove_turtle(self, turtle):
        """remove turtle function"""
        self.turtles.remove(turtle)

    def is_occupied(self):
        """judge occupied function"""
        i = 0
        while i < len(self.turtles):
            if isinstance(self.turtles[i], Cop):
                return True
            if isinstance(self.turtles[i], Agent) and self.turtles[i].is_jailed():
                return False
            i = i + 1
        return False

    def is_neighbour_with(self, patch):
        """judge neighbour function"""
        dx2 = pow(patch.x - self.x, 2)
        dy2 = pow(patch.y - self.y, 2)
        if sqrt(dx2 + dy2) <= VISION:
            return True
        return False


class PatchMap:
    """
    PatchMap class
    """

    def __init__(self, world):
        """init function"""
        self.patches = []
        self.world = world

        y = 0
        while y < MAP_HEIGHT:
            x = 0
            while x < MAP_WIDTH:
                self.patches.append(Patch(x, y))
                x += 1
            y += 1

        # Pre-calculate all neighbour patches
        i = 0
        while i < len(self.patches):
            j = 0
            while j < len(self.patches):
                if self.patches[i] == self.patches[j]:
                    j += 1
                    continue
                if self.patches[i].is_neighbour_with(self.patches[j]):
                    self.patches[j].neighbour_patches.append(self.patches[i])
                j += 1
            i += 1

    def get_random_unoccupied_patch(self, patch):
        """
        get random unoccupied patch function
        """
        if patch is not None:
            patchs = PatchMap.get_neighbours(patch)
        else:
            patchs = self.patches
        unoccupied_patch_list = []
        for patch in patchs:
            if not patch.is_occupied():
                unoccupied_patch_list.append(patch)
        if len(unoccupied_patch_list) == 0:
            return None
        return random.choice(unoccupied_patch_list)

    @staticmethod
    def get_neighbours(patch):
        """get neighbours function"""
        return patch.neighbour_patches

    @staticmethod
    def filter_neighbour_turtles(patch, turtle_filter):
        """filter neighbour turtles function."""
        neighbour_patch = PatchMap.get_neighbours(patch)
        all_turtles = []
        i = 0
        while i < len(neighbour_patch):
            turtles = list(filter(turtle_filter, neighbour_patch[i].turtles))
            all_turtles += turtles
            i += 1
        return all_turtles




