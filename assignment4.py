import sys

score = 0
game_over = 1
friends = 1
all_empty = 0


def detect_same_colors(game_map, row, column, ball_list):
    neighbours = []
    neighbours.append([row, column])
    balls = []
    while neighbours:
        new_neighbours = []
        for pair in neighbours:  # there was still repetition so i get rid of them
            if pair not in new_neighbours:
                new_neighbours.append(pair)
        balls.extend(new_neighbours)
        neighbours_clone = new_neighbours[::]
        neighbours = []
        for i in neighbours_clone:
            compare = game_map[i[0]][i[1]]
            game_map[i[0]][i[1]] = " "
            try:
                if game_map[i[0]][i[1] + 1] == compare:
                    neighbours.append([i[0], i[1] + 1])
            except IndexError:
                pass
            if i[1] - 1 < 0:  # to prevent index being negative and cause repetition
                pass
            elif game_map[i[0]][i[1] - 1] == compare:
                neighbours.append([i[0], i[1] - 1])
            try:
                if game_map[i[0] + 1][i[1]] == compare:
                    neighbours.append([i[0] + 1, i[1]])
            except IndexError:
                pass
            if i[0] - 1 < 0:
                pass
            elif game_map[i[0] - 1][i[1]] == compare:
                neighbours.append([i[0] - 1, i[1]])
    [ball_list.append(compare) for i in balls]


def make_them_fall(game_map):  # make balls with empty space under them fall
    column_num = len(game_map[0])
    row_num = len(game_map)
    for row in reversed(range(row_num)):
        for column in range(column_num):
            if game_map[row][column] == " ":
                new_row = row - 1
                if new_row < 0:
                    break
                break_loop = 0
                while break_loop == 0:
                    try:
                        if game_map[new_row][column] == " ":
                            new_row -= 1
                            if new_row < 0:
                                break
                        else:
                            game_map[row][column] = game_map[new_row][column]
                            game_map[new_row][column] = " "
                            break_loop = 1
                    except IndexError:
                        break_loop = 1


def print_map(game_map):
    row_num = len(game_map)
    column_num = len(game_map[0])
    for i in range(row_num):
        for j in range(column_num):
            print(game_map[i][j], end=" ")
        print()


def gotta_stick_together(game_map):  # removes empty columns
    global all_empty
    column_num = len(game_map[0])
    row_num = len(game_map)
    del_element = []
    for column in range(column_num):
        if game_map[row_num - 1][column] == " ":  # only checking last row because firstly balls will fall down
            for row in range(row_num):
                del_element.append([row, column])
    try:
        for i in del_element:
            del game_map[i[0]][i[1]]
    except IndexError:
        all_empty = 1


def if_you_empty_you_lose(game_map):  # removes empty rows
    column_num = len(game_map[0])
    row_num = len(game_map)
    count = 0
    break_loop = ""
    del_row = []
    for row in range(row_num):
        for column in range(column_num):
            if game_map[row][column] == " ":
                count += 1
                if count == column_num:
                    del_row.append(row)
            else:
                break_loop = "break"
                break
        if break_loop == "break":  # firstly i make balls fall so if a row is not empty no need to look further
            break
        else:
            count = 0
    if del_row:
        count_row = max(del_row)
        while count_row != -1:
            del game_map[count_row]
            count_row -= 1


def is_game_over(game_map):
    global game_over
    column_num = len(game_map[0])
    row_num = len(game_map)
    break_loop = ""
    game_over = 0
    for row in reversed(range(row_num)):
        for column in range(column_num):
            compare = game_map[row][column]
            if compare != " ":
                try:
                    if game_map[row][column + 1] == compare:
                        game_over = 1
                        break_loop = "break"
                        break
                except IndexError:
                    pass
                if column - 1 < 0:
                    pass
                elif game_map[row][column - 1] == compare:
                    game_over = 1
                    break_loop = "break"
                    break
                try:
                    if game_map[row + 1][column] == compare:
                        game_over = 1
                        break_loop = "break"
                        break
                except IndexError:
                    pass
                if row - 1 < 0:
                    pass
                elif game_map[row - 1][column] == compare:
                    game_over = 1
                    break_loop = "break"
                    break
            if game_map[row][column] == "X":
                game_over = 1
                break_loop = "break"
                break
        if break_loop == "break":
            break


def does_cell_have_friends(game_map, row, column):  # checks if cell has neighbouring cells with same content
    global friends  # friends state if it equals to 1 it has friend if 0 it does not
    compare = game_map[row][column]
    break_loop = ""
    friends = 0
    while break_loop == "":
        try:
            if game_map[row][column + 1] == compare:
                friends = 1
                break
            else:
                break_loop = "break"  # to stop while loop if cell has no friends
        except IndexError:
            pass
        if column - 1 < 0:
            pass
        elif game_map[row][column - 1] == compare:
            friends = 1
            break
        try:
            if game_map[row + 1][column] == compare:
                friends = 1
                break
        except IndexError:
            pass
        if row - 1 < 0:
            pass
        elif game_map[row - 1][column] == compare:
            friends = 1
            break


def bomb(game_map, row, column, ball_list):
    column_num = len(game_map[0])
    row_num = len(game_map)
    game_map[row][column] = " "
    for i in range(column_num):
        if game_map[row][i] == "X":
            bomb(game_map, row, i, ball_list)
        ball_list.append(game_map[row][i])
        game_map[row][i] = " "
    for j in range(row_num):
        if game_map[j][column] == "X":
            bomb(game_map, j, column, ball_list)
        ball_list.append(game_map[j][column])
        game_map[j][column] = " "


def cal_score(ball_list):
    global score
    for i in ball_list:
        if i == "B":
            score += 9
        elif i == "G":
            score += 8
        elif i == "W":
            score += 7
        elif i == "Y":
            score += 6
        elif i == "R":
            score += 5
        elif i == "P":
            score += 4
        elif i == "O":
            score += 3
        elif i == "D":
            score += 2
        elif i == "F":
            score += 1
        elif i == "X":
            score += 0


def main():
    global game_over, friends, all_empty
    input_path = sys.argv[1]
    with open(input_path, "r") as input_file:
        user_map = list()
        for line in input_file:
            user_map.append(line.strip("\n").split())
    same_balls = []
    is_game_over(user_map)
    map_check = 1
    while game_over == 1:
        if map_check != 0:
            print()
            print_map(user_map)
            print("\nYour score is: {}\n".format(str(score)))
            map_check = 1
        else:
            map_check = 1
        row_int, column_int = input("Please enter a row and column number: ").split()
        row_int, column_int = int(row_int), int(column_int)
        if row_int > len(user_map) - 1 or column_int > len(user_map[0]) - 1:
            print("\nPlease enter a valid size!\n")
            map_check = 0
        elif user_map[row_int][column_int] == " ":
            print("\nPlease enter a valid size!\n")
            map_check = 0
        else:
            if user_map[row_int][column_int] == "X":
                same_balls = []
                bomb(user_map, row_int, column_int, same_balls)
                cal_score(same_balls)
                make_them_fall(user_map)
                gotta_stick_together(user_map)
                if all_empty == 1:
                    break
                if_you_empty_you_lose(user_map)
            else:
                does_cell_have_friends(user_map, row_int, column_int)
                if friends == 1:
                    same_balls = []
                    detect_same_colors(user_map, row_int, column_int, same_balls)
                    cal_score(same_balls)
                    make_them_fall(user_map)
                    gotta_stick_together(user_map)
                    if all_empty == 1:
                        break
                    if_you_empty_you_lose(user_map)
        is_game_over(user_map)
    print_map(user_map)
    print("\nYour score is: {}\n".format(str(score)))
    print("Game over!")


main()
