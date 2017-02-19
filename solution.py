assignments = []

ROWS = 'ABCDEFGHI'
COLS = '123456789'


def cross(a, b):
    "Cross product of elements in 'a' and elements in 'b'."
    return [s + t for s in a for t in b]

def concat(a, b):
    "Traverse throuh two lists paralley and concatanate elements"
    return [s + t for s, t in zip(a, b)]


# boxes in a sudoku board
boxes = cross(ROWS, COLS)

# row, column, square units and diagonals
row_units = [cross(r, COLS) for r in ROWS]
column_units = [cross(ROWS, c) for c in COLS]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = [concat(ROWS, COLS), concat(ROWS, reversed(COLS))]

# list of units
unitlist = row_units + column_units + square_units + diagonal_units

# units for each box
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)

# peers for each box
peers = dict((s, set(sum(units[s],[]))-{s}) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def _eliminate_naked_twins(twin_value, twin_peers, values):
    """Eliminate naked twin digits from peers
    Args:
        twin_value: value of the naked twin boxes in a unit
        twin_peers: peers of the twins within the unit
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        values with digits belong to naked twin removed
    """
    for digit in twin_value:
        for peer in twin_peers:
            if digit in values[peer]:
                values[peer] = values[peer].replace(digit, '')

    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    for unit in unitlist:
        candidates = [b for b in unit if len(values[b]) == 2]
        for i in range(0, len(candidates)):
            for j in range(i+1, len(candidates)):
                box1 = candidates[i]
                box2 = candidates[j]
                if values[box1] == values[box2]:
                    # Eliminate the naked twins as possibilities for their peers
                    peer_candidates = set(unit) - {box1, box2}
                    values = _eliminate_naked_twins(values[box1], peer_candidates, values)

    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    digits = '123456789'
    return dict((b, v if v != '.' else digits) for (b, v) in zip(boxes, grid))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in ROWS:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in COLS))
        if r in 'CF': print(line)
    return


def eliminate(values):
    """
        Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
        Input: A sudoku in dictionary form.
        Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values


def only_choice(values):
    """
        Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
        Input: A sudoku in dictionary form.
        Output: The resulting sudoku in dictionary form.
        """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False  ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values  ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        #visualize_assignments(assignments)

    except SystemExit:
        pass
    except Exception as exp:
        print(exp)
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
