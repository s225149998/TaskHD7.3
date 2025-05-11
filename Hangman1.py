import random
import csv
import os
import platform

# Word list for the hangman game
word_list = ["python", "hangman", "programming", "computer", "developer", "challenge", "algorithm", "function"]

# Function to load or create a CSV file to store scores
def load_scores():
    if not os.path.exists('scores.csv'):
        return []
    with open('scores.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        scores = list(reader)
    return scores

# Function to save scores into CSV file
def save_scores(scores):
    with open('scores.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(scores)

# Function to display the top 10 scores
def display_scores(scores):
    print("\nTop 10 Scores:")
    scores.sort(key=lambda x: int(x[1]))  # Sort scores by number of turns
    top_10_scores = scores[:10]
    for idx, score in enumerate(top_10_scores):
        print(f"{idx+1}. {score[0]} - {score[1]} turns")

# Hangman drawing based on incorrect guesses (including scaffold)
def draw_hangman(attempts):
    stages = [
        '''
           ------
           |    |
           |    
           |    
           |    
           |    
        ---|---
        ''',  # Stage 0 - No parts drawn, scaffold is ready

        '''
           ------
           |    |
           |    O
           |    
           |    
           |    
        ---|---
        ''',  # Stage 1 - Head drawn

        '''
           ------
           |    |
           |    O
           |    |
           |    
           |    
        ---|---
        ''',  # Stage 2 - Body drawn

        '''
           ------
           |    |
           |    O
           |   /|
           |    
           |    
        ---|---
        ''',  # Stage 3 - One arm drawn

        '''
           ------
           |    |
           |    O
           |   /|\\
           |    
           |    
        ---|---
        ''',  # Stage 4 - Both arms drawn

        '''
           ------
           |    |
           |    O
           |   /|\\
           |   /
           |    
        ---|---
        ''',  # Stage 5 - One leg drawn

        '''
           ------
           |    |
           |    O
           |   /|\\
           |   / \\
           |    
        ---|---
        ''',  # Stage 6 - Both legs drawn

        '''
           ------
           |    |
           |    O
           |   /|\\
           |   / \\
           |   |
        ---|---
        ''',  # Stage 7 - Extra body details

        '''
           ------
           |    |
           |    O
           |   /|\\
           |   / \\
           |   | |
        ---|---
        ''',  # Stage 8 - Neck or extra body detail

        '''
           ------
           |    |
           |    O
           |   /|\\
           |   / \\
           |   | |
           |  / 
        ---|---
        '''  # Stage 9 - Final stage, full hangman with scaffold and details
    ]
    
    # Cap the number of attempts to 10
    attempts = min(attempts, 9)
    
    return stages[attempts]

# Function to clear the console screen (works for both Windows and Unix-based systems)
def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")  # Windows
    else:
        os.system("clear")  # Unix-based (Linux, macOS)

# Function to start the Hangman game
def play_game():
    # Randomly select a word
    word = random.choice(word_list)
    word_display = ["_"] * len(word)
    guessed_letters = set()
    attempts = 0
    max_attempts = 10  # Max allowed attempts (set to 10)

    print("\nWelcome to Hangman!")
    print(f"The word has {len(word)} letters: {' '.join(word_display)}\n")

    while attempts < max_attempts:
        clear_screen()  # Clear the screen to update the game state

        # Draw the hangman and current game status
        print(draw_hangman(attempts))
        print(f"Guessed letters: {' '.join(sorted(guessed_letters))}")
        print(f"Current word: {' '.join(word_display)}")
        print(f"Remaining attempts: {max_attempts - attempts}")

        guess = input(f"Attempt {attempts + 1}/{max_attempts}. Guess a letter: ").lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a valid letter.")
            continue
        
        if guess in guessed_letters:
            print("You've already guessed that letter!")
            continue

        guessed_letters.add(guess)
        if guess in word:
            for i, letter in enumerate(word):
                if letter == guess:
                    word_display[i] = guess
            print(f"Good guess! The word is now: {' '.join(word_display)}")
        else:
            attempts += 1

        if "_" not in word_display:
            print(f"\nCongratulations! You've guessed the word: {word} in {attempts} turns!")
            return attempts

    print(f"\nYou've run out of attempts! The word was: {word}")
    return attempts

# Main function
def main():
    scores = load_scores()
    display_scores(scores)
    
    while True:
        score = play_game()
        name = input("\nEnter your name: ")
        scores.append([name, score])
        save_scores(scores)
        
        display_scores(scores)
        
        play_again = input("\nDo you want to play again? (y/n): ").lower()
        if play_again != 'y':
            print("Thank you for playing! Goodbye.")
            break

if __name__ == "__main__":
    main()
