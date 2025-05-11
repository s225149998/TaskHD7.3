import random
import csv
import os
import streamlit as st

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
    st.subheader("Top 10 Scores:")
    scores.sort(key=lambda x: int(x[1]))  # Sort scores by number of turns
    top_10_scores = scores[:10]
    for idx, score in enumerate(top_10_scores):
        st.write(f"{idx + 1}. {score[0]} - {score[1]} turns")

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

# Function to start the Hangman game
def play_game():
    # Randomly select a word
    word = random.choice(word_list)
    word_display = ["_"] * len(word)
    guessed_letters = set()
    attempts = 0
    max_attempts = 10  # Max allowed attempts (set to 10)

    st.subheader("Hangman Game")
    st.write(f"The word has {len(word)} letters: {' '.join(word_display)}")

    while attempts < max_attempts:
        # Draw the hangman and current game status
        st.markdown(draw_hangman(attempts))
        st.write(f"Guessed letters: {' '.join(sorted(guessed_letters))}")
        st.write(f"Current word: {' '.join(word_display)}")
        st.write(f"Remaining attempts: {max_attempts - attempts}")
        
        guess = st.text_input(f"Attempt {attempts + 1}/{max_attempts}. Guess a letter:", key=f"guess_input_{attempts}")

        if guess:
            guess = guess.lower()
            if len(guess) != 1 or not guess.isalpha():
                st.write("Please enter a valid letter.")
                continue
            
            if guess in guessed_letters:
                st.write("You've already guessed that letter!")
                continue

            guessed_letters.add(guess)
            if guess in word:
                for i, letter in enumerate(word):
                    if letter == guess:
                        word_display[i] = guess
                st.write(f"Good guess! The word is now: {' '.join(word_display)}")
            else:
                attempts += 1

            if "_" not in word_display:
                st.success(f"Congratulations! You've guessed the word: {word} in {attempts} turns!")
                return attempts

        if attempts == max_attempts:
            st.error(f"You've run out of attempts! The word was: {word}")
            return attempts

    return attempts

# Main function for the Streamlit app
def main():
    scores = load_scores()
    display_scores(scores)
    
    # Let the user start the game
    start_button = st.button("Start New Game")
    if start_button:
        score = play_game()
        name = st.text_input("\nEnter your name:", key="name_input")
        if name:
            scores.append([name, score])
            save_scores(scores)
            
            display_scores(scores)

        play_again = st.radio("Do you want to play again?", ("Yes", "No"))
        if play_again == "Yes":
            main()
        else:
            st.write("Thank you for playing! Goodbye.")

if __name__ == "__main__":
    st.title("Hangman Game with Streamlit")
    main()
#  streamlit run C:\Users\james\anaconda31\Lib\site-packages\ipykernel_launcher.py
