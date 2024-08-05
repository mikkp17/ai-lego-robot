import heapq
from sys import maxsize


class Node:

    competition_map = ""

    def __init__(self, robot_position: tuple[int, int], crate_positions: list[tuple[int, int]], parent=None, action=None, path_cost=0, competition_map=None):
        self.robot_position = robot_position
        self.crate_positions = crate_positions
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        self.manhattan_distance = -1
        self.boxes_not_in_goal = -1

        if parent:
            self.depth: int = parent.depth + 1

        if competition_map:
            Node.competition_map = competition_map

    def __lt__(self, other):
        assert isinstance(other, Node)
        return (self.boxes_not_in_goal, self.manhattan_distance) < (other.boxes_not_in_goal, other.manhattan_distance)

    def __repr__(self):
        return f"<Node robot={self.robot_position}, crates={self.crate_positions}>"

    def set_manhattan_distance(self, distance: int):
        assert isinstance(distance, int)
        self.manhattan_distance = distance

    def get_manhattan_distance(self) -> int:
        return self.manhattan_distance

    def set_boxes_not_in_goal(self, boxes):
        assert isinstance(boxes, int)
        self.boxes_not_in_goal = boxes

    def get_boxes_not_in_goal(self) -> int:
        return self.boxes_not_in_goal

    def get_action(self) -> str | None:
        """Returns the action of this Node (Can be none)"""
        return self.action

    def __eq__(self, other):
        assert isinstance(other, Node)
        return self.robot_position == other.robot_position and self.crate_positions == other.crate_positions

    def path(self):
        """Returns a list of nodes that form the path from root to current node"""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __hash__(self):
        return hash((self.robot_position, *self.crate_positions))


def search():
    """The generic search algorithm. The algorithm starts with an initial state and builds a fringe, and then for
    every item in the fringe, it will explore child nodes until a solution is found."""
    # The initial node gets built from a map read from a text file

    the_map, robot_position, crate_positions = generate_map()
    init_node = Node(robot_position, crate_positions, competition_map=the_map)

    goal_positions = find_goal_positions(init_node.competition_map)
    init_node.set_manhattan_distance(
        calculate_manhattan_distance(goal_positions, init_node))
    init_node.set_boxes_not_in_goal(
        calculate_boxes_not_in_goal(goal_positions, init_node))

    visited = {}

    # The initial node gets inserted into the fringe to start the algorithm
    fringe: list[Node] = []
    heapq.heapify(fringe)
    heapq.heappush(fringe, init_node)

    # As long as there are items in the fringe, keep searching for a solution
    while fringe:

        # Get the first node from the fringe

        node = heapq.heappop(fringe)

        # Check if the nodes state is equal to the goal state
        if goal_reached(node, goal_positions):
            return node.path()
        # Find the children of the node and store them in the fringe
        children = expand(node, goal_positions, visited)

        for child in children:
            child.set_manhattan_distance(
                calculate_manhattan_distance(goal_positions, child))
            child.set_boxes_not_in_goal(
                calculate_boxes_not_in_goal(goal_positions, child))
            heapq.heappush(fringe, child)


def expand(parent: Node, goal_positions, visited) -> list[Node]:
    """Expands the current node and returns a list of children (successors)"""
    children = []
    actions = allowed_actions(parent)

    for action in actions:
        next_robot, next_crates = do_action(parent, action, goal_positions)
        child = Node(next_robot, next_crates, parent,
                     action, parent.path_cost+1)
        if not is_visited(child, visited):
            children = insert_into(child, children)
    return children


def calculate_manhattan_distance(goal_pos, node: Node):
    distance = 0
    for x_crate, y_crate in node.crate_positions:
        minimum_distance = maxsize
        for x_goal, y_goal in goal_pos:
            if node.competition_map[x_goal][y_goal] == "J":
                if x_crate != x_goal or y_crate != y_goal:
                    continue
            manhattan_distance = abs(x_crate-x_goal)+abs(y_crate-y_goal)
            if manhattan_distance < minimum_distance:
                minimum_distance = manhattan_distance
        distance += minimum_distance
    distance += node.path_cost
    return distance


def calculate_boxes_not_in_goal(goal_pos, node: Node):
    boxes_not_in_goal = len(node.crate_positions)
    for crate_x, crate_y in node.crate_positions:
        for goal_x, goal_y in goal_pos:
            if crate_x == goal_x and crate_y == goal_y:
                boxes_not_in_goal -= 1

    return boxes_not_in_goal


def insert_into(node, queue: list):
    """Inserts a node into the given queue/array"""
    queue.insert(0, node)
    return queue


def allowed_actions(node: Node):
    """Returns a list of allowed actions from current state"""
    allowed = []
    i, j = node.robot_position
    crates = node.crate_positions
    if ((i - 1, j) in crates and node.competition_map[i - 2][j] == '.' or (i-1, j) in crates and node.competition_map[i - 2][j] == 'G') and (i-2, j) not in crates:
        allowed.append('U')
    elif (node.competition_map[i - 1][j] == '.' or node.competition_map[i - 1][j] == 'G') and (i-1, j) not in crates:
        allowed.append('u')

    if ((i, j+1) in crates and node.competition_map[i][j + 2] == '.' or (i, j+1) in crates and node.competition_map[i][j + 2] == 'G') and (i, j+2) not in crates:
        allowed.append('R')
    elif (node.competition_map[i][j + 1] == '.' or node.competition_map[i][j+1] == 'G') and (i, j+1) not in crates:
        allowed.append('r')

    if ((i+1, j) in crates and node.competition_map[i + 2][j] == '.' or (i+1, j) in crates and node.competition_map[i + 2][j] == 'G') and (i+2, j) not in crates:
        allowed.append('D')
    elif (node.competition_map[i + 1][j] == '.' or node.competition_map[i + 1][j] == 'G') and (i+1, j) not in crates:
        allowed.append('d')

    if ((i, j-1) in crates and node.competition_map[i][j - 2] == '.' or (i, j-1) in crates and node.competition_map[i][j - 2] == 'G') and (i, j-2) not in crates:
        allowed.append('L')
    elif (node.competition_map[i][j - 1] == '.' or node.competition_map[i][j-1] == 'G') and (i, j-1) not in crates:
        allowed.append('l')

    return allowed


def do_action(parent_node: Node, action: str, goal_positions):
    """Executes a given action on a given state, returning the resulting state
    MAKE THIS WORK WITH G AS WELL"""
    if len(action) > 1:
        raise Exception(f"Argument 'action' was longer than 1 char, {action}")
    i, j = parent_node.robot_position
    new_crate_positions = parent_node.crate_positions.copy()
    # print('\n\nFound M at [' + str(i) + '][' + str(j) + '], now performing action: ' + action)
    pushing = True
    if action.islower():
        pushing = False
    if action.lower() == 'u':
        if pushing:
            new_crate_pos = (i-2, j)
            new_crate_positions.remove((i-1, j))
            new_crate_positions.append(new_crate_pos)
        new_robot_pos = (i-1, j)
    if action.lower() == 'r':
        if pushing:
            new_crate_pos = (i, j+2)
            new_crate_positions.remove((i, j+1))
            new_crate_positions.append(new_crate_pos)
        new_robot_pos = (i, j+1)
    if action.lower() == 'd':
        if pushing:
            new_crate_pos = (i+2, j)
            new_crate_positions.remove((i+1, j))
            new_crate_positions.append(new_crate_pos)
        new_robot_pos = (i+1, j)
    if action.lower() == 'l':
        if pushing:
            new_crate_pos = (i, j-2)
            new_crate_positions.remove((i, j-1))
            new_crate_positions.append(new_crate_pos)
        new_robot_pos = (i, j-1)

    new_crate_positions.sort()
    return new_robot_pos, new_crate_positions


def find_goal_positions(map):
    goal_positions = []
    for i, line in enumerate(map):
        for j, char in enumerate(line):
            if char == 'G':
                goal_positions.append((i, j))
            j += 1
        i += 1
    return tuple(goal_positions)


# def is_visited(node: Node, visited: list[Node]):
#     if visited is not None:
#         if node in visited:
#             # for visited_node in visited:
#             #     # the crate operation wont be equal for the same crates, cause the tuple is not sorted
#             #     if visited_node.robot_position == node.robot_position and visited_node.crate_positions == node.crate_positions:
#             #         print("is in visited")
#             return True
#     visited.append(node)
#     return False

def is_visited(node: Node, visited: dict[Node, int]):
    if visited is not None:
        if visited.get(node) != None:
            return True

    visited[node] = 0
    return False


def goal_reached(node: Node, goal_positions):
    """Returns true if the current state is the goal state, otherwise false"""
    if all(x_y in node.crate_positions for x_y in goal_positions):
        return True


def generate_map():
    with open("competition_map.txt") as file:
        outer_array = []
        robot_pos = None
        crate_pos = []
        for i, line in enumerate(file):
            line = line.strip()
            inner_array = []
            for j, char in enumerate(line):
                if char == "M":
                    robot_pos = i, j
                    inner_array.append(".")
                    continue
                elif char == "J":
                    crate_pos.append((i, j))
                    inner_array.append(".")
                    continue
                inner_array.append(char)
            outer_array.append(inner_array)
    if robot_pos is None:
        raise Exception("Found no robot ('M' in map).")
    return outer_array, robot_pos, crate_pos


def print_map(node: Node):
    """Prints the current state of the map"""
    for i, array in enumerate(node.competition_map):
        for j, char in enumerate(array):
            if (i, j) == node.robot_position:
                print(f" {print_red('M')}", end="")
            elif (i, j) in node.crate_positions:
                print(f" {print_green('J')}", end="")
            else:
                print(" "+char, end="")
        print("\n")
    print('\n')


def print_red(text: str):
    assert isinstance(text, str)
    return f"\033[0;91m{text}\033[00m"


def print_green(text: str):
    assert isinstance(text, str)
    return f"\033[0;92m{text}\033[00m"


def run():
    path: list[Node] = search()
    for node in path:
        print_map(node)
    print('Solution: ')
    for node in path[1:]:
        print(node.get_action(), end='')
    print()
    print("Total amount of moves: ", end="")
    print(len(path))


if __name__ == '__main__':
    run()
