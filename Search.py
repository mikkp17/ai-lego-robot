class Node:
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

    def solution(self):
        """Returns the list of actions to go from root node to current node"""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Returns a list of nodes that form the path from root to current node"""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def display(self):
        print(self)


def generic_search():
    fringe = []
    initial_node = Node(generate_map())
    fringe = insert_into(initial_node, fringe)
    while fringe is not None:
        node = remove_first(fringe)
        if goal_reached(node.state):
            return node.path()
        children = expand(node)
        fringe = insert_all(children, fringe)


def expand(node):
    """Expands the current node and returns a list of children (successors)"""
    children = []
    actions = allowed_actions(node.state)
    for action in actions:
        next_state = do_action(node.state, action)
        child = Node(next_state, self, action, self.path_cost + 1)
        children = insert_into(child, children)
    return children


def insert_into(node, queue):
    """Inserts a node into the given queue/array"""
    queue.insert(0, node)
    return queue


def insert_all(list, queue):
    """Inserts the given list/array into another given list/array"""
    queue.extend(list)
    return queue


def remove_first(queue):
    """Removes the first element of the fringe (queue/array)"""
    return queue.pop(0)


def allowed_actions(state):
    """Returns a list of allowed actions from current state"""
    raise NotImplementedError


def do_action(state, action):
    """Executes a given action on a given state, returning the resulting state"""
    i = 0
    for line in state:
        j = 0
        for char in line:
            if char == 'M':
                print('\n\nFound M at [' + str(i) + '][' + str(j) + '], now performing action: ' + action)

                pushing = True
                if action.islower():
                    pushing = False

                if action.lower() == 'u':
                    if pushing:
                        print('Pushing crate up')
                    else:
                        print('Going up')
                if action.lower() == 'r':
                    if pushing:
                        print('Pushing crate right')
                    else:
                        print('Going right')
                if action.lower() == 'd':
                    if pushing:
                        print('Pushing crate down')
                    else:
                        old_pos = state[i+1][j]
                        state[i+1][j] = 'M'
                        state[i][j] = old_pos
                        return state
                if action.lower() == 'l':
                    if pushing:
                        print('Pushing crate left')
                    else:
                        print('Going left')
            j += 1
        i += 1
    return state


def goal_reached(state):
    """Returns true if the current state is the goal state, otherwise false"""
    raise NotImplementedError


def run():
    path = generic_search()
    print('Solution: ')
    for node in path:
        node.display()


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


if __name__ == '__main__':
    game_map = generate_map()
    print_map(game_map)
    # Testing coordinates:
    # print(game_map[8][5])

    state = do_action(game_map, 'd')
    print_map(state)
