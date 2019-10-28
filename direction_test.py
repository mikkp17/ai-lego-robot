DIRECTIONS = ['up', 'right', 'down', 'left']

current_direction = 'down'

solution = ['up', 'left', 'left', 'down', 'up', 'right', 'left', 'right', 'down']
moves = []


def find_direction_index(direction):
    index = 0
    for value in DIRECTIONS:
        if value.lower() == direction.lower():
            return index
        index += 1


def calculate_direction(next_direction):
    global current_direction
    current_direction_index = find_direction_index(current_direction)
    next_direction_index = find_direction_index(next_direction)

    if current_direction_index == next_direction_index:
        return 'Current direction is ' + current_direction + \
               ', and next direction is ' + next_direction + ' so I keep going forward'
    elif abs(current_direction_index - next_direction_index) == 2:
        current_direction_print = current_direction
        current_direction = next_direction
        return 'Current direction is ' + current_direction_print + \
               ', and next direction is ' + next_direction + ' so I turn around'
    elif current_direction_index - next_direction_index == 1 or current_direction_index - next_direction_index == -3:
        current_direction_print = current_direction
        current_direction = next_direction
        return 'Current direction is ' + current_direction_print + \
               ', and next direction is ' + next_direction + ' so I turn left'
    elif current_direction_index - next_direction_index == -1 or current_direction_index - next_direction_index == 3:
        current_direction_print = current_direction
        current_direction = next_direction
        return 'Current direction is ' + current_direction_print + \
               ', and next direction is ' + next_direction + ' so I turn right'


def run():
    print(solution)
    for pos in solution:
        moves.append(calculate_direction(pos))
    for move in moves:
        print(move)


run()
