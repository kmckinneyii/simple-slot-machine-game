import random


# --- Configuration / constants ---
# Maximum number of lines the player can bet on
MAX_LINES = 3
# Maximum and minimum allowed bet per line
MAX_BET = 100
MIN_BET = 1

# Visual layout of the slot machine (rows x cols)
ROWS = 3
COLS = 3


# symbol_count maps a symbol to how many times it should appear in the
# symbol pool used for random selection. Symbols with higher counts are
# more likely to appear on a spin.
symbol_count = {
    'A': 2,
    'B': 4,
    'C': 6,
    'D': 8
}


# symbol_values maps a symbol to its payout multiplier when a winning
# line is achieved. The value is multiplied by the bet to compute winnings.
symbol_values = {
    'A': 5,
    'B': 4,
    'C': 3,
    'D': 2
}


def check_winnings(columns, lines, bet, values):
    """
    Check each bet line for a winning combination.

    Args:
        columns: list of columns where each column is a list of symbols (cols x rows)
        lines: number of top lines the player bet on (1..MAX_LINES)
        bet: bet amount per line
        values: dict mapping symbol->value multiplier

    Returns:
        (winnings, winning_lines): total winnings (int) and a list of line numbers that won

    Behavior:
        A line is a win only if the symbol in that row is the same across
        ALL columns (i.e., every column has the same symbol at that row).
    """
    winnings = 0
    winning_lines = []

    # Iterate only over the number of lines the player bet on.
    for line in range(lines):
        # The symbol in the first column for this row is the candidate symbol
        # to compare with symbols in the same row of other columns.
        symbol = columns[0][line]

        # Check each column for this line; if any column differs we break
        # and this line is not a winning line.
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                # mismatch found -> this line is not winning
                break
        else:
            # If we didn't break from the loop, all columns matched for this line
            winnings += values[symbol] * bet
            # store 1-based line number for user-friendly output
            winning_lines.append(line + 1)

    return winnings, winning_lines


def get_slot_machine_spin(rows, cols, symbols):
    """
    Generate a random spin result as a list of columns. Each column is a list
    of symbols of length `rows`.

    Implementation detail: for each column we copy the full symbol pool and
    draw without replacement for that column (so the same symbol won't repeat
    within a single column unless it appears multiple times in the pool).
    """
    # Build the full pool of symbols according to their counts
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []
    # For each column, select `rows` symbols randomly without replacement
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            # remove chosen symbol so it's not picked again for this column
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)

    return columns


def print_slot_machine(columns):
    """
    Nicely print the slot machine columns row-by-row so the output looks like
    a standard slot machine (rows across, columns down).
    """
    # number of rows is determined by the length of a column
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            # print symbol with separators; keep same formatting for all columns
            if i != len(columns) - 1:
                print(column[row], end=' | ')
            else:
                print(column[row], end=' | ')

        # newline after each row
        print()


def deposit():
    """
    Prompt the user to deposit an initial balance. Validates input to ensure
    a positive integer is provided.

    Returns the deposited amount as an int.
    """
    while True:
        amount = input('What would you like to deposit? $')
        # isdigit ensures the input contains only digits (no decimals, no signs)
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print('Amount must be greater than 0.')
        else:
            print('Please enter a number.')

    return amount


def get_number_of_lines():
    """
    Ask the player how many lines they want to bet on (1..MAX_LINES). Validates
    the input and returns it as an int.
    """
    while True:
        lines = input(
            f'How many lines would you like to bet on (1-{MAX_LINES})? ')
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print('Enter a valid number of lines.')
        else:
            print('Please enter a number.')

    return lines


def bet_amount():
    """
    Prompt for bet amount per line, validating that it is within allowed
    MIN_BET and MAX_BET. Returns the bet as an int.
    """
    while True:
        amount = input('What would you like to bet on each line? $')
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f'Amount must be between {MIN_BET} and {MAX_BET}')
        else:
            print('Please enter a number.')

    return amount


def game(balance):
    """
    Conduct a single round of the slot machine game using the provided
    current `balance`.

    Steps:
      - Ask how many lines to bet on
      - Ask for bet per line and ensure total bet is affordable
      - Spin the slot machine and print result
      - Calculate winnings and return the net change (winnings - total_bet)
    """
    lines = get_number_of_lines()
    while True:
        bet = bet_amount()
        total_bet = bet * lines
        if total_bet > balance:
            # inform the player and let them choose another bet
            print(
                f'You do not have enough to bet that amount, your current balance is: ${balance}')

        else:
            break

    print(
        f'You are betting ${bet} on {lines} lines. Total bet is ${total_bet}')
    # produce the random columns for the spin
    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    # determine winnings and which lines (if any) won
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_values)
    print(f'You won ${winnings}.')
    print(f'You won on lines:', *winning_lines)
    # return net result: positive if player won more than bet, negative otherwise
    return winnings - total_bet


def main():
    """
    Entry point for the script. Prompts for an initial deposit then repeatedly
    plays rounds until the player quits. Keeps track of the player's balance.
    """
    balance = deposit()
    while True:
        print(f'Current balance is ${balance}')
        answer = input('Press enter to play (q to quit).')
        if answer == 'q':
            break
        balance += game(balance)

    print(f'You left with ${balance}')


main()
