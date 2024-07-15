import random #pseudorandom library for picking of an integer
secret_number = random.randint(1, 20) #picking a random number

user_guess = int(input("Guess what the secret integer betweem 1 and 20 is ")) #The initial guess of the game, must convert variable to type integer for comparison
guesses = 0
while True: #the loop for the guesses
    guesses += 1 #counting up the guesses, using only 1 for the whole script
    if user_guess > secret_number: #directing the player if the guess is too high
        print(f"Your guess is higher than the secret number. Guess again. (You've guessed {guesses} times.)") #telling the player he's wrong and to guess again
       # user_guess = int(input("Guess again (a number less than " + str(user_guess) + "): ")) #asking the player for a new number
    elif user_guess < secret_number: #if the player guesses too low
        print(f"Your guess is lower than the secret number. Guess again. (You've guessed {guesses} times.)") #notifying the player he's wrong and how many guesses
       # user_guess = int(input("Guess again (a number greater than " + str(user_guess) + "): ")) #giving the player another chance to guess
    elif user_guess == secret_number: #if the player guesses correctly
        print(f"Good job! You guessed the number in {guesses} guesses.")
        break #finishing the game, ending the loop
    user_guess = int(input("Guess again")) #asking the player for a new number