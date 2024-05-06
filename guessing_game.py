import random #so that we can call a pseudorandom number
import sys #so that we can use the sys.exit function

def menu(user_choice):#this is the function that will be used to call the menu, such that when a player guesses a 
    while True:
        if user_choice not in ['x', 's', 'n']: #first checks that input is a valid menu option, then offers the menu if it isn't
            print("Invalid input. Please choose a valid menu option.")
            user_choice = input("Enter 'n' to start a new game, 'x' to exit, or 's' to show the secret number: ").lower() #automatically makes the input lowercase
        if user_choice == 'x':
            print("Exiting the game. Thanks for playing!")
            sys.exit()  # Exit the program if the user chooses to exit
        elif user_choice == 's':
            print(f"Cheat code activated: The number is {secret_number}")
            return 'break'
        elif user_choice == 'n':
            print("new game started")
            new_game() #actually start a new game by calling the function to change the number
            return 'new_game'  # Return 'new_game' to indicate starting a new game
        elif user_choice.isdigit():
            return user_choice, 'break'



def new_game(): # Function to start a new game by picking a new secret number
    global secret_number  # Access the global variable secret_number (so that all instances of secret_number will be changed)
    secret_number = random.randint(1, 20)
    print("A new game has started. Good luck!")

def play_game(user_input):
    guesses = 0
    while True:
        if user_input.isdigit():
            user_guess = int(user_input)
            guesses += 1 #one counter for the whole game
            if user_guess == secret_number:
                print(f"Good job! You guessed the number in {guesses} guesses.")
                return
            elif user_guess > secret_number:
                print(f"Your guess is higher than the secret number. Guess again. (You've guessed {guesses} times.)")
            else:
                print(f"Your guess is lower than the secret number. Guess again. (You've guessed {guesses} times.)")
        else:
            choice = menu(user_input)  # Call menu function if input is not numeric
        user_input = input("Guess what the secret integer between 1 and 20 is: ")

def main():
    print("Welcome to the Number Guessing Game!")
    while True:
        new_game()  # Start a new game
        while True:
            user_input = input("Guess what the secret integer between 1 and 20 is or enter a character to enter the menu: ")
            if user_input.isdigit():  # Check if user input is numeric
                play_game(user_input)  # Call play_game function if user input is numeric
                break  # Exit the loop once the game is played
            else: #if the input isn't numeric, it will enter the menu function
                menu(user_input) #automatically puts the user_input into the menu function

main() #starts the program from the main function. If we don't have this the program won't start
