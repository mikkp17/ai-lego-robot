import copy


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
        return self.action

    def path(self):
        """Returns a list of nodes that form the path from root to current node"""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))


def generic_search():
    fringe = []
    initial_node = Node(generate_map())
    fringe = insert_into(initial_node, fringe)
    while fringe is not None:
        top_node = remove_first(fringe)
        if goal_reached(top_node.state):
            return top_node.path()
        children = expand(top_node)
        fringe = insert_all(children, fringe)


def expand(parent):
    """Expands the current node and returns a list of children (successors)"""
    children = []
    actions = allowed_actions(parent.state)
    for action in actions:
        parent_state = copy.deepcopy(parent.state)
        next_state = do_action(parent_state, action)
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
    return queue


def remove_first(queue):
    """Removes the first element of the fringe (queue/array)"""
    return queue.pop(0)


def allowed_actions(state):
    """Returns a list of allowed actions from current state"""
    allowed = []
    i, j = find_current_pos(state)

    if state[i - 1][j] == '.':
        allowed.append('u')
    elif state[i - 1][j] == 'J' and state[i - 2][j] == '.':
        allowed.append('U')

    if state[i][j + 1] == '.':
        allowed.append('r')
    elif state[i][j + 1] == 'J' and state[i][j + 2] == '.':
        allowed.append('R')

    if state[i + 1][j] == '.':
        allowed.append('d')
    elif state[i + 1][j] == 'J' and state[i + 2][j] == '.':
        allowed.append('D')

    if state[i][j - 1] == '.':
        allowed.append('l')
    elif state[i][j - 1] == 'J' and state[i][j - 2] == '.':
        allowed.append('L')

    return allowed


def do_action(state, action):
    """Executes a given action on a given state, returning the resulting state"""
    i, j = find_current_pos(state)
    # print('\n\nFound M at [' + str(i) + '][' + str(j) + '], now performing action: ' + action)
    pushing = True
    if action.islower():
        pushing = False
    if action.lower() == 'u':
        if pushing:
            old_crate_pos = state[i - 2][j]
            state[i - 2][j] = 'J'
            state[i - 1][j] = old_crate_pos
        old_pos = state[i - 1][j]
        state[i - 1][j] = 'M'
        state[i][j] = old_pos
    if action.lower() == 'r':
        if pushing:
            old_crate_pos = state[i][j + 2]
            state[i][j + 2] = 'J'
            state[i][j + 1] = old_crate_pos
        old_pos = state[i][j + 1]
        state[i][j + 1] = 'M'
        state[i][j] = old_pos
    if action.lower() == 'd':
        if pushing:
            old_crate_pos = state[i + 2][j]
            state[i + 2][j] = 'J'
            state[i + 1][j] = old_crate_pos
        old_pos = state[i + 1][j]
        state[i + 1][j] = 'M'
        state[i][j] = old_pos
    if action.lower() == 'l':
        if pushing:
            old_crate_pos = state[i][j - 2]
            state[i][j - 2] = 'J'
            state[i][j - 1] = old_crate_pos
        old_pos = state[i][j - 1]
        state[i][j - 1] = 'M'
        state[i][j] = old_pos
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


def goal_reached(state):
    """Returns true if the current state is the goal state, otherwise false"""
    if state[7][2] == 'J' and state[8][2] == 'M':
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
    path = generic_search()
    for node in path:
        print_map(node.state)
    print('Solution: ')
    for node in path[1:]:
        print(node.solution(), end='')


if __name__ == '__main__':
    run()
