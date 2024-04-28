import random #pseudorandom library for picking of an integer
secret_number = random.randint(1, 20) #picking a random number

user_guess = int(input("Guess what the secret integer betweem 1 and 20 is ")) #The initial guess of the game, must convert variable to type integer for comparison

while True: #the loop for the guesses
    if user_guess > secret_number: #directing the player if the guess is too high
        guesses = guesses + 1 #counting up
        print(f"Your guess is higher than the secret number. Guess again. (You've guessed {guesses} times.)") #telling the player he's wrong and to guess again
        user_guess = int(input("Guess again (a number less than " + str(user_guess) + "): ")) #asking the player for a new number
    elif user_guess < secret_number: #if the player guesses too low
        guesses = guesses + 1 #counter
        print(f"Your guess is lower than the secret number. Guess again. (You've guessed {guesses} times.)") #notifying the player he's wrong and how many guesses
        user_guess = int(input("Guess again (a number greater than " + str(user_guess) + "): ")) #giving the player another chance to guess
    elif user_guess == secret_number: #if the player guesses correctly
        guesses = guesses + 1 #still have to count for every guess
        print(f"Good job! You guessed the number in {guesses} guesses.")
        break #finishing the game, ending the loop
