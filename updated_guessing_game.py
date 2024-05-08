import random
import sys #needed for the sys.exit function

def menu(user_choice, secret_number):
    while True:
        if user_choice not in ['x', 's', 'n']:
            print("Invalid input. Please choose a valid menu option.")
            user_choice = input("Enter 'n' to start a new game, 'x' to exit, or 's' to show the secret number: ").lower()
        if user_choice == 'x':
            print("Exiting the game. Thanks for playing!")
            sys.exit()
        elif user_choice == 's':
            print(f"Cheat code activated: The number is {secret_number}")
            return 'break'
        elif user_choice == 'n':
            print("new game started")
            return 'new_game'
        elif user_choice.isdigit():
            return user_choice, 'break'

def new_game():
    secret_number = random.randint(1, 20)
    print("A new game has started. Good luck!")
    return secret_number

def play_game(user_input, secret_number):
    guesses = 0
    while True:
        if user_input.isdigit():
            user_guess = int(user_input)
            guesses += 1
            if user_guess == secret_number:
                print(f"Good job! You guessed the number in {guesses} guesses.")
                return
            elif user_guess > secret_number:
                print(f"Your guess is higher than the secret number. Guess again. (You've guessed {guesses} times.)")
            else:
                print(f"Your guess is lower than the secret number. Guess again. (You've guessed {guesses} times.)")
        else:
            choice = menu(user_input, secret_number)
            if choice == 'new_game':
                guesses = 0
                secret_number = new_game()
        user_input = input("Guess what the secret integer between 1 and 20 is: ")

def main():
    print("Welcome to the Number Guessing Game!")
    while True:
        secret_number = new_game()
        while True:
            user_input = input("Guess what the secret integer between 1 and 20 is or enter a character to enter the menu: ")
            if user_input.isdigit():
                play_game(user_input, secret_number)
                break
            else:
                menu(user_input, secret_number)

main()
