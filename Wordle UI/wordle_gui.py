import random
from tkinter import *
from tkinter import ttk
import string


class WordleBoard:


    def __init__(self):
        """Initializes the WordleBoard object."""
        self.secret_words, self.all_words = self.get_words()
        self.chosen_word = random.choice(self.secret_words).upper()
        self.all_guesses = []
        self.letters_remaining = list(string.ascii_uppercase)
        self.found = False
        self.num_guesses = 0


    def get_words(self):
        """Read the words from the dictionary files.
        We assume the two required files are in the current working directory.
        The file with the words that may be picked as the secret words is
        assumed to be names secret_words.txt. The file with the rest of the
        words that are valid user input but will not be picked as the secret
        word are assumed to be in a file named other_valid_words.txt.
        Returns a sorted tuple with the words that can be
        chosen as the secret word and a set with ALL the words,
        including both the ones that can be chosen as the secret word
        combined with other words that are valid user guesses.
        """
        temp_secret_words = []
        with open("secret_words.txt", "r") as data_file:
            all_lines = data_file.readlines()
            for line in all_lines:
                temp_secret_words.append(line.strip().upper())
        temp_secret_words.sort()
        secret_words = tuple(temp_secret_words)
        all_words = set(secret_words)
        with open("other_valid_words.txt", "r") as data_file:
            all_lines = data_file.readlines()
            for line in all_lines:
                all_words.add(line.strip().upper())
        return secret_words, all_words


    def win_inputs(self):
        """
        Prints the ending outputs based on if word was correctly guessed and 
        in how many attempts
        """
        if not self.found:
            return "Not quite. The secret word was " + self.chosen_word + "."
        elif self.num_guesses == 6:
            return "You win. Phew!"
        elif self.num_guesses == 4:
            return "You win. Splendid!"
        elif self.num_guesses == 3:
            return "You win. Impressive!"
        elif self.num_guesses == 2:
            return "You win. Magnificent!"
        elif self.num_guesses == 1:
            return "You win. Genius!"
        else:
            return "You win. Great!"


    def take_input(self):
        """
        Takes in guesses from the user and ensures the validity of the
        guess.
        """
        input_valid = False
        while not input_valid:
            guess = input("\nEnter your guess. A 5 letter word: ").upper()
            print()
            if guess in self.all_words:
                input_valid = True
            else:
                print(guess + " is not a valid word. Please try again.")
        self.num_guesses += 1
        return guess


    def evaluate_input(self, guess):
        """
        Evaluates the input that the user provides against the secret 
        word.
        """
        guess_arr = []
        for char in guess:
            guess_arr += char

        # Evaluates the guess and creates the output string.
        cur_output = []
        for char in range(5):
            cur_output += "-"
        repeated_letters = {}
        successful_letters = {}
        index = 0
        for cur_char in guess_arr:
            cur_output = self.eval_logic(
                repeated_letters,
                successful_letters,
                index,
                guess_arr,
                cur_char,
                cur_output
            )
            index += 1
        self.handle_repeats(
            repeated_letters, 
            successful_letters, 
            cur_output
        )
        if guess == self.chosen_word:
            self.found = True
        return cur_output


    def final_prints(
        self,
        guess, 
        cur_output
    ):
        """Prints out the required text at the end of each guess."""
        cur_output_str = ""
        for cur_str in cur_output:
            cur_output_str += cur_str
        self.all_guesses.append(cur_output_str)
        self.all_guesses.append(guess)
        for out in self.all_guesses:
            print(out)

        # Prints unused letters.
        print("\nUnused letters:", end="")
        for cur_letter in self.letters_remaining:
            print(" ", end="")
            print(cur_letter, end="")
        print()
        if guess == self.chosen_word:
            return True
        return False


    def eval_logic(
        self,
        repeated_letters,
        successful_letters,
        index,
        guess_arr,
        cur_char,
        cur_output,
    ):
        """
        Helper function for evaluate input that is the main 
        driver logic determing how close a guess was to the secret word.
        """

        # Handles if current char corresponds to correctly indexed letter 
        # in the secret word
        successful_list = list(successful_letters.values())
        if guess_arr[index] == self.chosen_word[index]:
            cur_output[index] = "G"
            successful_letters[index] = cur_char

        # Handle if theres a repeated letter in the guess.
        elif (cur_char in self.chosen_word) and ((cur_char in 
                guess_arr[index + 1:]) or (cur_char in guess_arr[0: index])):
            repeated_letters[index] = cur_char

        # Handles if char is in the word but in wrong place with no repeats in 
        # guess.
        elif (
            (cur_char in self.chosen_word)
            and (cur_char not in successful_list)
            and (cur_char not in guess_arr[index + 1 :])
        ):
            cur_output[index] = "O"

        # Updates the letters remaining printout.
        if cur_char in self.letters_remaining:
            self.letters_remaining.remove(cur_char)
        return cur_output


    def handle_repeats(
        self,
        repeated_letters, 
        successful_letters, 
        cur_output
    ):
        """Handles more than one of the same letter in a guess. Helper function 
        for eval_logic.
        """

        # Adds letters that weren't correctly guessed into a dictionary.
        unsuccessful_letters = {}
        for i in range(5):
            if i not in successful_letters:
                unsuccessful_letters[i] = self.chosen_word[i]

        for avoid_index in repeated_letters:
            cur_char = repeated_letters[avoid_index]

            # Creating indexes from the secret word if the index contains the 
            # desired char.
            secret_indexes = []
            for i in range(len(self.chosen_word)):
                if self.chosen_word[i] == cur_char and (i in 
                                    unsuccessful_letters
                                     ):
                    secret_indexes.append(i)

            if len(secret_indexes) > 0:
                cur_output[avoid_index] = "O"
                unsuccessful_letters.pop(secret_indexes[0])
        

def main():
    root = Tk()
    root.title("Mastermind")
    root.resizable(False, False)
    new_game(root, WordleBoard(), [], [])
    root.mainloop()


def set_letter(board, letter_vars, let, guess, info_var):
    """Sets the letter variable to the letter that was pressed."""
    if board.found or board.num_guesses >= 6:
        letter_var = info_var.set("Game over. Please start a new game.")
    else: 
        letter_var = letter_vars[board.num_guesses][len(guess)]
        let = let.upper()
        if let.isalpha():
            letter_var.set(let)
            guess.append(let)


def key_response(root, labels, guess, board, letter_vars, info_var):
    """Sets up the key bindings for the game.
    """
    alpha_bindings = list(string.ascii_letters)
    print(alpha_bindings)

    # Bind enter and backspace to lambda functions that call enter_guess and
    # undo_last_pick
    root.bind('<Return>', lambda event: enter_guess(board, guess, 
                                                    info_var, labels))
    root.bind('<BackSpace>', lambda event: undo_last_pick(board, 
                                                          guess, letter_vars))
    
    # Bind each letter to a lambda function that calls set_letter
    for i in range(len(alpha_bindings)):
        root.bind(
            alpha_bindings[i], 
            lambda event: set_letter(
            board, 
            letter_vars,
            event.char, 
            guess, 
            info_var
        ))
        

def update_guess(guess, color, labels, board):
    """Updates the guess with letter typed and updates the labels."""
    if len(guess) < 4 and not board.game_over():
        guess.append(color[0])
        labels[board.num_guesses][len(guess) - 1].configure(bg=color)


def create_labels(root, letter_vars):
    """Create the frame for the feedback.
    The feedback variables shall be used to show the result of the guess.
    """
    label_frame = ttk.Frame(root, padding="150 3 3 3")
    label_frame.grid(row=1, column=1)
    label_frame.update()
    labels = []
    for row in range(1, 7):
        label_row = []
        letter_row = []
        for col in range(1, 6):
            letter_var = StringVar()

            label = Label(
                label_frame, 
                font='Courier 32 bold', 
                text=' ', 
                textvariable=letter_var, 
                width = 1,
                borderwidth=1, 
                relief='solid'
            )
            label.grid(row=row, column=col, padx=2, pady=2)
            label_row.append(label)
            letter_row.append(letter_var)
        labels.append(label_row)
        letter_vars.append(letter_row)
    return labels


def create_control_buttons(root, labels, guess, board, letter_vars, info_var):
    """Create the main control buttons to undo a guess and
    enter a guess. Also, a label for information to show user.
    """
    bottom_frame = ttk.Frame(root)
    bottom_frame.grid(row=2, column=1, columnspan=2)

    # To give the user information on errors and inform them when they win.
    new_game_button = Button(bottom_frame, font='Arial 24 bold',
                             text='New Game',
                             command=lambda: new_game(
                                                root, 
                                                board, 
                                                labels, 
                                                guess,
                                            ))
    new_game_button.grid(row=1, column=0, padx=5, pady=5)
    undo_button = Button(
                        bottom_frame, 
                        font='Arial 24 bold',
                        text='Undo Choice',
                        command=lambda: undo_last_pick(
                                                board, 
                                                guess, 
                                                letter_vars
                                            ))
    undo_button.grid(row=1, column=1, padx=5, pady=5)
    enter_guess_button = Button(bottom_frame, font='Arial 24 bold',
            text='Enter Guess',
            command=lambda: enter_guess(board, guess, info_var, labels))
    enter_guess_button.grid(row=1, column=2, padx=5, pady=5)
    info_label = ttk.Label(bottom_frame, font='Arial 16 bold',
                           textvariable=info_var)
    info_label.grid(row=2, column=0, columnspan=2)


def new_game(root, board, labels, guess):
    """Starts a new game."""
    board = WordleBoard()

    # 2D array of letter_vars per each label in the board
    letter_vars = []
    labels = create_labels(root, letter_vars)

    # A string that stores users current guess
    guess = []
    info_var = StringVar()
    key_response(root, labels, guess, board, letter_vars, info_var) 
    create_control_buttons(root, labels, guess, board, letter_vars, info_var)


def enter_guess(board, guess, info_var, labels):
    """Enters the guess and updates the labels."""
    if len(guess) == 5:
        guess_string = ''.join(guess)
        if guess_string not in board.all_words:
            info_var.set("I don't know that word.")
        else: 
            guess.clear()
            feedback = board.evaluate_input(guess_string)
            for i in range(len(feedback)):
                if feedback[i] == 'G':
                    labels[board.num_guesses][i].config(bg='green')
                elif feedback[i] == 'O':
                    labels[board.num_guesses][i].config(bg='orange')
                elif feedback[i] == '-':
                    labels[board.num_guesses][i].config(bg='gray')
            board.num_guesses += 1
            if len(feedback) == 0:
                feedback = 'NONE'
            if board.found:  # They won!
                info_var.set(board.win_inputs())
            elif board.num_guesses >= 6:  # Game is over.
                info_var.set(board.win_inputs())
    else:
        if board.found or board.num_guesses >= 6:
            info_var.set('Game over. Please start a new game.')
        else:
          info_var.set('Must have 5 letters to make guess.')


def undo_last_pick(board, guess, letter_vars):
    """Undo the last pick by the user if there is one or more guesses for
    the current row.
    """
    if len(guess) >= 1:
        row = board.num_guesses
        column = len(guess) - 1
        letter_vars[row][column].set(' ')
        guess.pop()


def text_main():
    board = WordleBoard()
    while not board.found:
        guess = input('Enter guess: ').upper()
        board.make_guess(guess)
        print(board)

    if board.found:
        print('You won!')
    else:
        board.win_inputs()


if __name__ == '__main__':
    main()

