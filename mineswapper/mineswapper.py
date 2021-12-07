from random import shuffle


def correct_field(num_of_rows, num_of_columns, mines_number) -> bool:

    if all(i.isdigit() for i in [num_of_rows, num_of_columns, mines_number]):
        if int(num_of_rows) > 0 and int(num_of_columns) > 0 and int(mines_number) > 0:
            return True
    print('Пожалуйста, введите верные данные')
    return False


def correct_input(xy: list, field: list) -> bool:

    if len(xy) == 2 \
            and all(isinstance(i, int) for i in xy) \
            and all(i >= 0 for i in xy) \
            and xy[0] <= len(field[0]) - 1 and xy[1] <= len(field) - 1:
        return True
    print('Пожалуйста, введите верные координаты')
    return False


def is_mine(field: list, x: int, y: int) -> bool:

    if field[x][y] == 1:
        return True
    return False


def open_values(image: list) -> int:
    count_cell = 0

    for i in image:
        for j in i:
            if j != '#':
                count_cell += 1
    return count_cell


def calculate_value(field: list, x: int, y: int) -> int:
    mines = 0

    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= x + i < len(field) and 0 <= y + j < len(field[0]) and not (i == 0 and j == 0):
                if field[x + i][y + j] == 1:
                    mines += 1
    return mines


def new_image(field: list, image: list, x: int, y: int) -> list:

    new_value = calculate_value(field, x, y)
    image[x][y] = str(new_value)
    return image


def failed_image(field: list, image: list) -> list:

    for i, sublist in enumerate(field):
        for j, cell in enumerate(sublist):
            if cell == 1:
                image[i][j] = '*'
    return image


def show_image(image):
    for i in image:
        print(' '.join(i))


def make_move(field: list, image: list):
    x, y = int(input('Введите номер строки: ')), int(input('Введите номер столбца: '))
    xy = [x, y]
    if not correct_input(xy, field):
        return image, True

    # is clicked ???
    # if yes
        # return image, True

    if is_mine(field, x, y):
        print('Game over')
        image = failed_image(field, image)
        return image, False
    else:
        image = new_image(field, image, x, y)
        return image, True


def generate_field(num_of_rows: int, num_of_columns: int, mines_number: int) -> list:
    present_field = []
    temp_list = []
    image = [['#' for i in range(int(num_of_rows))] for j in range(int(num_of_columns))]
    field = [0] * (int(num_of_rows) * int(num_of_columns) - int(mines_number)) + [1] * int(mines_number)
    shuffle(field)
    for i, j in enumerate(field):
        if not (i + 1) % int(num_of_columns):
            temp_list.append(j)
            present_field.append(temp_list)
            temp_list = []
        else:
            temp_list.append(j)

    return present_field, image


def is_finish():
    pass


def start_game():

    num_of_rows, num_of_columns = input('Введите кол-во строк: '), input('Введите кол-во столбцов: ')
    mines_number = input('Введите количество мин: ')
    if correct_field(num_of_rows, num_of_columns, mines_number):
        field, image = generate_field(num_of_rows, num_of_columns, mines_number)
    else:
        start_game()

    game_status = True

    while game_status:
        if open_values(image) == int(num_of_rows) * int(num_of_columns) - int(mines_number):
            print('Победа!')
            failed_image(field, image)
            game_status = False
        else:
            show_image(image)
            image, game_status = make_move(field, image)
    show_image(image)


def is_new_game() -> bool:
    pass


def main():
    #while is_new_game():
    start_game()


main()
