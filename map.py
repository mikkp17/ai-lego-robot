file = open("competition_map.txt", 'r')
if file.mode == 'r':
    file_content = file.readlines()

    # Make an empty 2d array
    width = len(file_content[0])
    height = len(file_content)
    comp_map = [[0 for x in range(width)] for y in range(height)]

    # Populate the comp_map with actual competition map
    i = 0
    while i < len(file_content):
        arr = list(file_content[i].strip())
        comp_map[i] = arr
        i += 1
    # Printing the array
    for lines in comp_map:
        print(lines)

else:
    print("must be in read mode")
