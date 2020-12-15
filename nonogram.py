from typing import *

# constants representing the different options for a square
BLACK = 1
WHITE = 0
MAYBE = -1

# constant that hold the position of each set of constraints
ROW_CONSTRAINTS = 0
COL_CONSTRAINTS = 1

# a dictionary holding symbols for each state for printing and debugging
SYMBOLS = {BLACK: " * ", WHITE: "   ", MAYBE: " / "}

# aliases for readability
Blocks = List[int]
Constraints = List[Blocks]
FullConstraints = List[Constraints]
Row = List[int]
Board = List[Row]


def print_board(board: Board, msg: str = ""):
    """
    prints board for visualization and debug purposes
    :param board: the board to print
    :param msg: a message to add with the print
    :return: None
    """
    print("--------------------------------------------------------------")
    board_str = ""
    for row in board:
        for box in row:
            board_str += SYMBOLS[box]

        board_str += "\n"
    print(msg+"\n"+board_str)
    print("--------------------------------------------------------------")


def get_maybe_count(board: Board) -> int:
    """
    counts how many MAYBE tiles are on the board. use when checking if a board
    is finished
    :param board: the board we are checking
    :return:the amount of MAYBE tiles on the board
    """
    return sum([row.count(MAYBE) for row in board])


def row_variations(row: Row, blocks: Blocks) -> List[Row]:
    """
    returns all possible variations of a row based on its current data and
    its constraints
    :param row: the row to get its variations
    :param blocks: list of constraints for the row
    :return: list of variations of the row
    """
    if not row:
        return []
    return row_variations_helper(row, blocks, [])


def row_variations_helper(row: Row, blocks: Blocks,
                          variations: List[Row]) -> List[Row]:
    """
    recursive helper function.
    :param row: the row to get its variations
    :param blocks: list of constraints for the row
    :param variations: list that the variations are appended to
    :return: list of variations for the row
    """
    if not is_valid_variation(row, blocks):
        return []

    if MAYBE not in row:
        variations.append(row[:])
        return variations

    ind = row.index(MAYBE)
    for i in range(2):
        row[ind] = i
        row_variations_helper(row, blocks, variations)
    row[ind] = -1
    return variations


def is_valid_variation(row: Row, blocks: Blocks) -> bool:
    """
    check whether a row variation is valid according to the row's constraints
    :param row: the row in the current variation
    :param blocks: the constraints of the row
    :return: True if the variation is valid, False otherwise
    """
    # if there are no MAYBEs in the row, check its validity
    if row.count(MAYBE) == 0:
        return check_row_validity(len(row), row, blocks)

    # if there aren't enough possibilities for BLACK or too many BLACKS
    if row.count(BLACK)+row.count(MAYBE) < sum(blocks) or \
            row.count(BLACK) > sum(blocks):
        return False

    if BLACK not in row:
        return row.count(MAYBE) >= sum(blocks)
    else:
        return row.count(BLACK) + row.count(MAYBE) >= sum(blocks)


def check_row_validity(n: int, row: Row, blocks: Blocks) -> bool:
    """
    recursive function that checks if a given row or a given part of a row
    is valid. unklike is_valid_variation, this function is called for rows
    without MAYBE fillings.
    The function searches for the nearest black square and checks it length
    than calls itself again from after the full black part
    :param n: length of row
    :param row: the row we are checking
    :param blocks: the constraints of the row
    :return: True if the row/part of the row is valid according to its
    constraints
    """
    # if this is a full row but there aren't enough blacks return False
    if len(row) == n and row.count(BLACK) != sum(blocks):
        return False

    if not blocks:
        return BLACK not in row
    if BLACK not in row:
        return True

    black_ind = row.index(BLACK)

    if WHITE in row[black_ind:]:
        white_ind = row[black_ind:].index(WHITE) + black_ind
    else:
        if len(row[black_ind:]) > blocks[0]:
            return False
        else:
            return True

    if white_ind - black_ind != blocks[0]:
        return False

    return check_row_validity(n, row[white_ind:], blocks[1:])


def get_options(n: int, blocks: Blocks, org_n: int) -> List[Row]:
    """
    recursive function that builds all possible options for a row with a certain
    length according to given constraints
    :param n: the length of the part being build (start as the length of the
    full row)
    :param blocks: the constraints of the row
    :param org_n: the length of the full row
    :return: all possible options for a row according to its constraints
    """
    if n == 0:
        return []
    if n == 1:
        return [[WHITE],[BLACK]]

    all_options = []
    for option in get_options(n-1, blocks, org_n):
        for i in range(2):
            added_options = option+[i]
            if check_row_validity(org_n, added_options, blocks):
                all_options.append(added_options)

    return all_options


def constraint_satisfactions(n: int, blocks: Blocks) -> List[Row]:
    """
    return a list of all possible rows with a given length
    according to given constraints
    :param n: the length of the row
    :param blocks: the constraints of the row
    :return: a list of possible rows
    """
    if not blocks:
        return [[0]*n]
    options = get_options(n, blocks, n)
    return options


def intersection_row(rows: List[Row]) -> Row:
    """
    combines a list of rows into one general row
    If there are two different none-MAYBE values for a certain square, the
    function will place a MAYBE and move to next square
    If a certain square only hold MAYBEs and a single kind of filling, the
    function will place the filling in the square
    :param rows: the rows to intersect
    :return: the intersection of the rows
    """
    if not rows:
        return []
    intersection = rows[0][:]
    for i in range(len(intersection)):
        for row in rows:
            if intersection[i] == MAYBE:
                if row[i] != MAYBE:
                    intersection[i] = row[i]
            elif row[i] != MAYBE and intersection[i] != row[i]:
                intersection[i] = MAYBE
                break

    return intersection


def get_row(n: int, constraints: Blocks) -> Row:
    """
    uses other functions to create a single row that is an intersection of
    all of the possible variations according to a set of constraints
    :param n: the length of the row
    :param constraints: the constraints of the row
    :return: the created row
    """
    rows = constraint_satisfactions(n, constraints)
    if constraints and not rows:
        return []
    return intersection_row(rows)


def fill_all_rows(n: int, constraints: List[Blocks]) -> Board:
    """
    create a full board according to the constraints of its rows
    :param n: the length of the board's rows
    :param constraints: the constraints for each row of the board
    :return: a board with rows according to the constraints
    """
    board = []
    for i in range(len(constraints)):
        row_constraints = constraints[i]
        row = get_row(n, row_constraints)
        if not row:
            return []
        board.append(row)

    return board


def apply_row_constraints(board: Board, row_constraints: Constraints) -> Board:
    """
    apply the row constraints on a board
    :param board: the board to be changes
    :param row_constraints: the constraints of the rows
    :return: the board after changes were applied
    """
    new_board: Board = []
    for i, row in enumerate(board):
        variations = row_variations(row, row_constraints[i])
        intersection = intersection_row(variations)
        if not variations:
            return []
        new_board.append(intersection)

    return new_board


def apply_col_constraints(board: Board, col_constraints: Constraints) -> Board:
    """
        apply the column constraints on a board
        :param board: the board to be changes
        :param col_constraints: the constraints of the rows
        :return: the board after changes were applied
        """
    if not board:
        return []
    flipped_board = flip_board(board)
    flipped_board = apply_row_constraints(flipped_board, col_constraints)
    if not flipped_board:
        return []
    return flip_board(flipped_board)


def create_by_constraints(constraints: FullConstraints) -> Board:
    """
    creates a full board according to the full set of constraints given
    :param constraints:
    :return: a board built according to the constraints
    """
    rows = fill_all_rows(len(constraints[COL_CONSTRAINTS]),
                         constraints[ROW_CONSTRAINTS])
    board = apply_col_constraints(rows, constraints[COL_CONSTRAINTS])
    if not board:
        return []
    return board


def flip_board(board: Board) -> Board:
    """
    "flips" a board (turns it columns to rows and vis versa)
    :param board: the board to flip
    :return: the flipped board
    """
    new_board = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if i == 0:
                new_board.append([board[i][j]])
            else:
                new_board[j] += [board[i][j]]
    return new_board


def is_board_valid(board: Board, constraints: FullConstraints) -> bool:
    """
    checks validity of board by checking its rows' and columns' validity
    :param board: the board to check
    :param constraints: the constraints of the board
    :return: True of the board is valid, False otherwise
    """
    if not board:
        return False

    for i in range(len(board)):
        if not is_valid_variation(board[i], constraints[0][i]):
            return False
    cols = flip_board(board)
    for i in range(len(cols)):
        if not is_valid_variation(cols[i], constraints[1][i]):
            return False

    return True


def solve_easy_nonogram(constraints: FullConstraints) -> Board:
    """
    solves easy nonograms
    :param constraints: the board constraints
    :return: the solved board
    """
    board = create_by_constraints(constraints)
    return solve_easy_helper(constraints, board)


def solve_easy_helper(constraints: FullConstraints, board: Board)\
        -> Board:
    """
    helper recursive function that solves easy nonograms by applying constraints
    again and again until the board is either invalid or finished
    :param constraints: board constraints
    :param board: the current state of the board
    :return: a board after changes have been applied
    """
    if not board or not is_board_valid(board, constraints):
        return []

    if get_maybe_count(board) == 0:
        return board

    new_board = apply_row_constraints(board, constraints[0])
    new_board = apply_col_constraints(new_board, constraints[1])
    if new_board == board:
        return board
    else:
        new_board = solve_easy_helper(constraints, new_board)
        return new_board


def solve_nonogram(constraints: FullConstraints) -> List[Board]:
    """
    solves complicated nonograms with multiple possible solutions
    :param constraints: the constraints of the board
    :return: a list of possible solutions
    """
    print(len(constraints[0]),len(constraints[1]))
    board = create_by_constraints(constraints)
    if not board:
        return []
    return solve_nonogram_helper(constraints, board, [])


def solve_nonogram_helper(constraints: FullConstraints,
                          board: Board, solutions) -> List[Board]:
    """
    recursive helper function. solves the board by creating possible variations
    of each row reaching all solutions of each variations using backtracking
    :param constraints: the full set of constraints for the board
    :param board: the current state of the board
    :param solutions: list to append solutions to
    :return: a list of solutions
    """

    # print_board(board)

    if not board or board in solutions or not is_board_valid(board, constraints):
        return []

    if get_maybe_count(board) == 0:
        solutions.append(board[:])

    for i, row in enumerate(board):
        if MAYBE in board[i]:
            variations = row_variations(row, constraints[ROW_CONSTRAINTS][i])
            for variation in variations:
                if variation != board[i]:
                    board[i] = variation
                    new_board = apply_col_constraints(board, constraints[COL_CONSTRAINTS])
                    solve_nonogram_helper(constraints, new_board, solutions)

    return solutions