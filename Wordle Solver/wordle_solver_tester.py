from wordle_solver import WordleSolver
import time
import random
import string


def main():
    """Plays a text based version of Wordle.
    1. Read in the words that can be choices for the secret word
    and all the valid words. The secret words are a subset of
    the valid words.
    2. Explain the rules to the player.
    3. Get the random seed from the player if they want one.
    4. Play rounds until the player wants to quit.
    """
    all_words = get_words()
    keep_playing = True
    welcome_and_instructions()
    """Plays game continuously until user wants it to end"""
    round_count = 0
    average_guesses = [0]
    not_solved = 0
    solver_time = 0
    solver = WordleSolver()
    while round_count < 20:
        all_guesses = []
        feedback = []
        letters_remaining = list(string.ascii_uppercase)
        chosen_word = random.choice(all_words).upper()
        num_guesses = 0
        found = False
        while num_guesses < 7 and not found:
            start_time = time.time()
            guess = solver.get_guess(feedback)
            end_time = time.time()
            solver_time += end_time - start_time
            found = evaluate_input(
                all_guesses, 
                letters_remaining, 
                guess,
                chosen_word,
                feedback
                )
            num_guesses += 1
            feedback.append(guess)
        if not found:
            not_solved += 1
        win_inputs(num_guesses, found, chosen_word, average_guesses)
        round_count += 1
    print(average_guesses)
    print("Round Count:", end=" ")
    print(round_count)
    average_guesses[0] = average_guesses[0] / round_count
    print(average_guesses)
    print(solver_time)
    print("not solved:", end=" ")
    print(not_solved)


def welcome_and_instructions():
    """
    Print the instructions and set the initial seed for the random
    number generator based on user input.
    """
    print("Welcome to Wordle.")
    instructions = input("\nEnter y for instructions, anything else to skip: ")
    if instructions == "y":
        print("\nYou have 7 chances to guess the secret 7 letter word.")
        print("Enter a valid 7 letter word.")
        print("Feedback is given for each letter.")
        print("G indicates the letter is in the word and in the correct spot.")
        print("O indicates the letter is in the word but not that spot.")
        print("- indicates the letter is not in the word.")
    set_seed = input("\nEnter y to set the random seed, anything else to skip: ")
    if set_seed == "y":
        random.seed(int(input("\nEnter number for initial seed: ")))


def get_words():
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
    all_words = []
    with open("all_words_7.txt", "r") as data_file:
        all_lines = data_file.readlines()
        for line in all_lines:
            all_words.append(line.strip().upper())
    return all_words


def win_inputs(num_guesses, found, chosen_word, average_guesses):
    """
    Prints the ending outputs based on if word was correctly guessed and in 
    how many attempts
    """
    if not found:
        print("\nNot quite. The secret word was " + chosen_word + ".")
        print()
    elif num_guesses == 7:
        average_guesses[0] += 7
        print("barely made it you win")
    elif num_guesses == 6:
        average_guesses[0] += 6
        print("\nYou win. Phew!\n")
    elif num_guesses == 4:
        average_guesses[0] += 4
        print("\nYou win. Splendid!\n")
    elif num_guesses == 3:
        average_guesses[0] += 3
        print("\nYou win. Impressive!\n")
    elif num_guesses == 2:
        average_guesses[0] += 2
        print("\nYou win. Magnificent!\n")
    elif num_guesses == 1:
        average_guesses[0] += 1
        print("\nYou win. Genius!\n")
    else:
        average_guesses[0] += 5
        print("\nYou win. Great!\n")


def evaluate_input(all_guesses, letters_remaining, guess, chosen_word, feedback):
    """Evaluates the input that the user provides against the secret word."""
    guess_arr = []
    for char in guess:
        guess_arr += char

    # Evaluates the guess and creates the output string.
    cur_output = []
    for char in range(7):
        cur_output += "-"
    repeated_letters = {}
    successful_letters = {}
    index = 0
    for cur_char in guess_arr:
        cur_output = eval_logic(
            repeated_letters,
            successful_letters,
            index,
            guess_arr,
            cur_char,
            letters_remaining,
            chosen_word,
            cur_output
        )
        index += 1
    handle_repeats(
        repeated_letters, 
        successful_letters, 
        chosen_word, 
        cur_output
    )
    return final_prints(
        all_guesses, 
        guess, 
        letters_remaining, 
        chosen_word, 
        cur_output,
        feedback
    )


def final_prints(
    all_guesses, 
    guess, 
    letters_remaining, 
    chosen_word, 
    cur_output,
    feedback
):
    """Prints out the required text at the end of each guess."""
    cur_output_str = ""
    for cur_str in cur_output:
        cur_output_str += cur_str
    all_guesses.append(cur_output_str)
    feedback.append(cur_output_str)
    all_guesses.append(guess)
    for out in all_guesses:
        print(out)

    # Prints unused letters.
    print("\nUnused letters:", end="")
    for cur_letter in letters_remaining:
        print(" ", end="")
        print(cur_letter, end="")
    print()
    if guess == chosen_word:
        return True
    return False


def eval_logic(
    repeated_letters,
    successful_letters,
    index,
    guess_arr,
    cur_char,
    letters_remaining,
    chosen_word,
    cur_output,
):
    """
    Helper function for evaluate input that is the main driver logic determing
    how close a guess was to the secret word.
    """

    # Handles if current char corresponds to correctly indexed letter in the 
    # secret word
    successful_list = list(successful_letters.values())
    if guess_arr[index] == chosen_word[index]:
        cur_output[index] = "G"
        successful_letters[index] = cur_char

    # Handle if theres a repeated letter in the guess.
    elif (cur_char in chosen_word) and ((cur_char in guess_arr[index + 1:]) or 
    (cur_char in guess_arr[0: index])
    ):
        repeated_letters[index] = cur_char

    # Handles if char is in the word but in wrong place with no repeats in 
    # guess.
    elif (
        (cur_char in chosen_word)
        and (cur_char not in successful_list)
        and (cur_char not in guess_arr[index + 1 :])
    ):
        cur_output[index] = "O"

    # Updates the letters remaining printout.
    if cur_char in letters_remaining:
        letters_remaining.remove(cur_char)
    return cur_output


def handle_repeats(
    repeated_letters, 
    successful_letters, 
    chosen_word, 
    cur_output
):
    """
    Handles more than one of the same letter in a guess. Helper function for
    eval_logic.
    """

    # Adds letters that weren't correctly guessed into a dictionary.
    unsuccessful_letters = {}
    for i in range(7):
        if i not in successful_letters:
            unsuccessful_letters[i] = chosen_word[i]

    for avoid_index in repeated_letters:
        cur_char = repeated_letters[avoid_index]

        # Creating indexes from the secret word if the index contains the 
        # desired char.
        secret_indexes = []
        for i in range(len(chosen_word)):
            if chosen_word[i] == cur_char and i in unsuccessful_letters:
                secret_indexes.append(i)

        if len(secret_indexes) > 0:
            cur_output[avoid_index] = "O"
            unsuccessful_letters.pop(secret_indexes[0])


def cont_game():
    """Determines if player wants to continue playing after the round ends."""
    cont_in = input("Do you want to play again? Type Y for yes: ")
    return True


if __name__ == "__main__":
    main()
