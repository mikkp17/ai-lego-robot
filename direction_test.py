DIRECTIONS = ['u', 'r', 'd', 'l']

current_direction = 'd'

solution = ['L', 'd', 'l', 'l', 'l', 'u', 'u', 'u', 'u', 'R', 'R', 'd', 'r', 'U', 'U', 'U', 'U', 'd', 'd', 'd',
            'l', 'l', 'l', 'd', 'd', 'r', 'U', 'l', 'u', 'R', 'R', 'd', 'r', 'U', 'U', 'U', 'r', 'u', 'L', 'L',
            'L', 'u', 'l', 'D', 'r', 'r', 'r', 'd', 'd', 'd', 'd', 'l', 'l', 'l', 'd', 'd', 'd', 'r', 'U', 'U',
            'U', 'l', 'u', 'R', 'R', 'd', 'r', 'U', 'U', 'U', 'r', 'u', 'L', 'd', 'd', 'd', 'd', 'l', 'l', 'd',
            'd', 'd', 'r', 'r', 'u', 'L', 'd', 'l', 'U', 'U', 'U', 'l', 'u', 'R', 'R', 'd', 'r', 'U', 'U', 'U',
            'r', 'u', 'u', 'L', 'L', 'L', 'r', 'D', 'R', 'u', 'r', 'D']
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
    print('Last direction is ' + current_direction + ' and now I stop')


run()
