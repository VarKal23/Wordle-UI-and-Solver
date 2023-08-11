import random
import string
class WordleSolver:


    def __init__(self):
        self.__all_words = []
        self.words_left = set()
        self.get_words()


    def handle_g(self, g_indexes, cur_guess, cur_word, remove_words):
        """
        Determines if current word needs to be removed from words_left set
        based on 'G' indexes in feedback and the current guess
        """
        for g in g_indexes:
            if cur_guess[g] != cur_word[g]:
                remove_words.add(cur_word.lower())
                return True
        return False
    

    def handle_o(self, o_indexes, cur_word, cur_guess, remove_words):
        """
        Determines if current word needs to be removed from words_left set
        based on 'O' indexes in feedback and the current guess
        """
        for o in o_indexes:
            if (cur_guess[o] == cur_word[o]) or (cur_guess[o] not in cur_word):
                remove_words.add(cur_word.lower())
                return True
        return False

    
    def handle_d(
            self, 
            dash_indexes, 
            cur_guess, 
            remove_words, 
            g_indexes, 
            cur_word, 
            o_indexes
        ):
        """
        Determines if current word needs to be removed from words_left set
        based on '-' indexes in feedback and the current guess
        """
        for d in dash_indexes:
            if cur_word[d] == cur_guess[d]:
                remove_words.add(cur_word.lower())
                return True
            
            num_char_count = 0
            for cur_char in cur_word:
                if cur_char == cur_guess[d]:
                    num_char_count += 1
            correct_count = 0
            
            for n in range(7):
                if (cur_guess[n] == cur_guess[d]) and (n in g_indexes or 
                                                       n in o_indexes):
                    correct_count += 1

            if num_char_count != correct_count:
                remove_words.add(cur_word.lower())
                return True
        return False
        

    def guess_algo(self, cur_guess, g_indexes, o_indexes, dash_indexes):
        """
        Starts algorithm to determine the guess to output
        """

        # Update the words left list according to feedback
        remove_words = set()
        for cur_word in self.words_left:

            # compare each letter in curword vs curfeedback
            cur_word = cur_word.upper()
            removed = False
            removed = self.handle_g(
                g_indexes, 
                cur_guess, 
                cur_word, 
                remove_words
            )
            if removed:
                continue
            removed = self.handle_o( 
                o_indexes, 
                cur_word, 
                cur_guess, 
                remove_words
            )
            if removed:
                continue
            self.handle_d(
                dash_indexes, 
                cur_guess, 
                remove_words, 
                g_indexes, 
                cur_word, 
                o_indexes
            )

        for word_to_remove in remove_words:
            self.words_left.remove(word_to_remove)

        return self.words_left.pop().upper()       


    def get_guess(self, feedback):
        """
        Make a guess for the current round of Wordle.
        :param feedback: A list of strings representing the guesses so far
        and the feedback for those guesses in the current game of Wordle.
        If feedback is empty then this is the first guess.
        The order of the elements of feedback is [feedback_1, guess_1,
        feedback_2, guess_2, ...]
        All strings are length 7.
        The feedback strings consist of G, O, and -.
        G for GREEN, correct letter in correct spot.
        O for letter in word but not in right spot.
        - for letter not in word.
        :return: A string that is in __all_words and is the next guess.
        """
        if len(feedback) < 1:
            self.words_left = []
            self.__all_words = []
            self.get_words()
            return "ELASTIC"
        else:
            cur_feedback = feedback[len(feedback) - 2]
            cur_guess = feedback[len(feedback) - 1]
            g_indexes = []
            o_indexes = []
            dash_indexes = []
            for letter_index in range(7):
                if cur_feedback[letter_index] == 'G':
                    g_indexes.append(letter_index)
                elif cur_feedback[letter_index] == 'O':
                    o_indexes.append(letter_index)
                elif cur_feedback[letter_index] == '-':
                    dash_indexes.append(letter_index)

        print(len(self.words_left))
        return self.guess_algo(
            cur_guess, 
            g_indexes, 
            o_indexes, 
            dash_indexes
        )


    def get_words(self):
        """ Read the words from the dictionary file and place them
        in the __all_words instance variable.
        We assume the  required files are in the current working directory
        and is named all_words_5.txt. We also assume all words are
        seven letters long, one word per line.
        Returns a set of strings with all the words from the file.
        """
        with open('all_words_7.txt', 'r') as data_file:
            all_lines = data_file.readlines()
            self.words_left = set()
            for line in all_lines:
                self.__all_words.append(line.strip())
                self.words_left.add(line.strip())


    def show_words(self):
        """
        Debugging method to check file was read in correctly.
        :return: None
        """
        print(len(self.__all_words))
        for word in self.__all_words:
            print(word)
'''
From a high level, my approach was developed with the goal of narrowing down
the list of possible words as quick as possible using the given feedback from
the game. Before I used algorithms to evaluate the feedback, I found the 
indexes of each 'G', 'O', and '-' for use in my algorithm. I then called my 
actual guess_algo function which iterated through each word in a words left 
list which is initially the list of all the possible words. I then had separate 
functions handling each 'G', 'O', and '-' feedback letter/index and would try 
to find the fastest way to eliminate a word from the words_left set. 

In my handle_g function
I iterated through each 'G' index from the feedback and compared the letter at 
the certain index in the current guess against the current word in the set of 
words_left. If the letters at g indexes in the current guess didn't match up 
with those in the cur_word in the words_left set I would add the word to a list 
of words that would be removed from the set. If the word was set to be removed 
from the set then the for loop would go on to compare the next word against the
feedback, else it would go on to check the 'O' indexes. In the handle_o 
function theres a for loop that goes through the indexes of the 'O' 's in the 
feedback and checks to see if the letter at the index of an 'O' in the current 
guess is equal to the letter at the index or if the letter at the index in the 
guess isn't present in the current word. If either condition is met then it 
adds the current word to a list of words to be removed. If the current word is 
added to the list of words to be removed then the next word in words_left will 
be evaluated, else we will move on to evaluate the current word against the 
'-' 's in the feedback. 

In handle_dash function we iterate through the index of each dash in the given 
feedback and at the beginning we had a quick check to see if the character at 
the dash index in the current guess was equal to the character at the dash 
index in the current word, and if so we would add the word to our list of words
to be removed and end the function/move on to word removal. If the characters 
weren't equal, we would go through all the characters of both the current guess 
and current word checking if they were equal to the character at the index in 
cur_guessand part of the 'G' or 'O' indexex array, and if both these conditions 
were met we would increment a counter. There were 2 separate counters, one for 
the guess and one for the current word and after iterating through both words, 
if the counters didn't equal eachother then we would add the current word to 
the list of words to remove. My logic here was that if the current letter in 
the guess at the dash index was a dash, that meant it was either not in the 
word or it had repeated letters that corresponded to a 'G' index or prior 
letters that corresponded to an 'O' index, so counting the total 'G's and 'O's 
and comparing the amount in the guess vs the current word would tell me if the 
current word could still be a potential correct answer.

After all the words in the words_left set have been evaluated against these
conditions, I popped a word from the set and returned it as a guess.

My Results:
Total Rounds: 2000
Rounds Not Solved: 11
Total Guesses: 7476
Average Guesses Per Round: 3.738
Solver Time elapsed: 60.38
Rounds Per Second = 33


'''
