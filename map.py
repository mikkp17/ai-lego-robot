# File to open competition_map and populate an array
file = open("competition_map.txt", 'r')
if file.mode == 'r':
    file_content = file.readlines()

    # Make a 2d array and populate with 0
    width = len(file_content[0])
    height = len(file_content)
    competition_map = [[0 for x in range(width)] for y in range(height)]

    # Populate the competition_map with actual competition map
    counter = 0
    while counter < len(file_content):
        competition_map[counter] = list(file_content[counter].strip())
        counter += 1
    # Printing the array
    for line in competition_map:
        print(line)

else:
    print("must be in read mode")