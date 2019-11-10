import copy  # Used to deepcopy our 2D array of state


class Node:
    """A Node is a representation of an object in the tree. In Sokoban, each Node represents a state of the game,
    and each of those nodes holds information about their parent nodes (previous moves) as well as what action they
    did to get there from their parent node. A Node also keeps track of how expensive the path has been so far,
    and how deep down the tree it is (how many moves it took to get there). """

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def get_action(self):
        """Returns the action of this Node (Can be none)"""
        return self.action

    def path(self):
        """Returns a list of nodes that form the path from root to current node"""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))


def search():
    """The generic search algorithm. The algorithm starts with an initial state and builds a fringe, and then for
    every item in the fringe, it will explore child nodes until a solution is found."""
    # The initial node gets built from a map read from a text file
    initial_node = Node(generate_map())
    goal_positions = find_goal_positions(initial_node.state)

    # The initial node gets inserted into the fringe to start the algorithm
    fringe = []
    fringe = insert_into(initial_node, fringe)

    # As long as there are items in the fringe, keep searching for a solution
    while fringe is not None:

        # Get the first node from the fringe
        node = remove_first(fringe)

        # Check if the nodes state is equal to the goal state
        if goal_reached(node.state, goal_positions):
            return node.path()

        # Find the children of the node and store them in the fringe
        children = expand(node, goal_positions)
        '''
        Make this list a priority queue based on h(n) to achieve A* search.
        h(n) is distance between crates and goal, if crates are closer, expand those nodes first.
        Can also sort nodes by distance from player to a crate with a smaller coefficient to achieve even smarter search
        '''
        fringe = insert_all(children, fringe)


def expand(parent, goal_positions):
    """Expands the current node and returns a list of children (successors)"""
    children = []
    actions = allowed_actions(parent.state)
    for action in actions:
        parent_state = copy.deepcopy(parent.state)
        next_state = do_action(parent_state, action, goal_positions)
        child = Node(next_state, parent, action, parent.path_cost + 1)
        children = insert_into(child, children)
    return children


def insert_into(node, queue):
    """Inserts a node into the given queue/array"""
    queue.insert(0, node)
    return queue


def insert_all(first_list, second_list):
    """Inserts the first list into the second list"""
    second_list.extend(first_list)
    return second_list


def remove_first(queue):
    """Removes the first element of the fringe (queue/array)"""
    return queue.pop(0)


def allowed_actions(state):
    """Returns a list of allowed actions from current state
    MAKE THIS WORK WITH G AS WELL"""
    allowed = []
    i, j = find_current_pos(state)

    if state[i - 1][j] == '.' or state[i - 1][j] == 'G':
        allowed.append('u')
    elif state[i - 1][j] == 'J' and state[i - 2][j] == '.' or state[i - 1][j] == 'J' and state[i - 2][j] == 'G':
        allowed.append('U')

    if state[i][j + 1] == '.':
        allowed.append('r')
    elif state[i][j + 1] == 'J' and state[i][j + 2] == '.' or state[i][j + 1] == 'J' and state[i][j + 2] == 'G':
        allowed.append('R')

    if state[i + 1][j] == '.':
        allowed.append('d')
    elif state[i + 1][j] == 'J' and state[i + 2][j] == '.' or state[i + 1][j] == 'J' and state[i + 2][j] == 'G':
        allowed.append('D')

    if state[i][j - 1] == '.':
        allowed.append('l')
    elif state[i][j - 1] == 'J' and state[i][j - 2] == '.' or state[i][j - 1] == 'J' and state[i][j - 2] == 'G':
        allowed.append('L')

    return allowed


def do_action(state, action, goal_positions):
    """Executes a given action on a given state, returning the resulting state
    MAKE THIS WORK WITH G AS WELL"""
    i, j = find_current_pos(state)
    # print('\n\nFound M at [' + str(i) + '][' + str(j) + '], now performing action: ' + action)
    pushing = True
    if action.islower():
        pushing = False
    if action.lower() == 'u':
        if pushing:
            state[i - 2][j] = 'J'
        state[i - 1][j] = 'M'
    if action.lower() == 'r':
        if pushing:
            state[i][j + 2] = 'J'
        state[i][j + 1] = 'M'
    if action.lower() == 'd':
        if pushing:
            state[i + 2][j] = 'J'
        state[i + 1][j] = 'M'
    if action.lower() == 'l':
        if pushing:
            state[i][j - 2] = 'J'
        state[i][j - 1] = 'M'
    if (i, j) in goal_positions.values():
        state[i][j] = 'G'
    else:
        state[i][j] = '.'
    return state


def find_current_pos(state):
    i = 0
    for line in state:
        j = 0
        for char in line:
            if char == 'M':
                return i, j
            j += 1
        i += 1
    return -1, -1


def find_goal_positions(state):
    goal_positions = {}
    i = 0
    for line in state:
        j = 0
        for char in line:
            if char == 'G':
                goal_positions[len(goal_positions)] = i, j
            j += 1
        i += 1
    return goal_positions


def goal_reached(state, goal_positions):
    """Returns true if the current state is the goal state, otherwise false"""
    lst = []
    for goal in goal_positions.values():
        i, j = goal
        lst.append(state[i][j])
    if all('J' in state for state in lst):
        return True


def generate_map():
    """Generates the initial map from a supplied text file and returns it as a 2D array"""
    file = open("competition_map.txt")
    outer_array = []
    for line in file:
        line.strip()
        inner_array = []
        for char in line:
            inner_array.append(char)
        outer_array.append(inner_array)
    file.close()
    return outer_array


def print_map(state):
    """Prints the current state of the map"""
    for array in state:
        for char in array:
            print(' ' + char, end='')
    print('\n')


def run():
    path = search()
    for node in path:
        print_map(node.state)
    print('Solution: ')
    for node in path[1:]:
        print(node.get_action(), end='')


if __name__ == '__main__':
    run()
