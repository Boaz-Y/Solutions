import random
import sys
import tkinter as tk
from tkinter import messagebox

class numberguess:
    def __init__(self, master):
        self.master = master
        master.title("Number Guessing Game")

        self.secret_number = self.new_game()
        self.guesses = 0

        self.label = tk.Label(master, text="Guess the number between 1 and 20:")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()
        self.entry.bind("<Return>", self.enter_pressed)

        self.guess_button = tk.Button(master, text="Guess", command=self.guess_number)
        self.guess_button.pack()

        self.new_game_button = tk.Button(master, text="New Game", command=self.start_new_game)
        self.new_game_button.pack()

        self.show_number_button = tk.Button(master, text="Show Number", command=self.show_secret_number)
        self.show_number_button.pack()

        self.exit_button = tk.Button(master, text="Exit", command=self.exit_game)
        self.exit_button.pack()

        self.message = tk.Label(master, text="", fg="red")
        self.message.pack()

        self.counter_label = tk.Label(master, text="Guesses: 0")
        self.counter_label.pack()

    def new_game(self):
        return random.randint(1, 20)

    def start_new_game(self):
        self.secret_number = self.new_game()
        self.guesses = 0
        self.message.config(text="")
        self.counter_label.config(text="Guesses: 0")
        self.entry.delete(0, tk.END)
        messagebox.showinfo("New Game", "A new game has started. Good luck!")

    def guess_number(self):
        user_input = self.entry.get()
        if user_input.isdigit():
            user_guess = int(user_input)
            self.guesses += 1
            self.counter_label.config(text=f"Guesses: {self.guesses}")
            if user_guess == self.secret_number:
                self.message.config(text=f"Good job! You guessed the number in {self.guesses} guesses.")
            elif user_guess > self.secret_number:
                self.message.config(text=f"Your guess is higher than the secret number. Try again.")
            else:
                self.message.config(text=f"Your guess is lower than the secret number. Try again.")
        else:
            self.message.config(text="Invalid input. Please enter a number between 1 and 20.")
        self.entry.delete(0, tk.END)

    def enter_pressed(self, event):
        self.guess_number()

    def show_secret_number(self):
        messagebox.showinfo("Secret Number", f"The secret number is {self.secret_number}")

    def exit_game(self):
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = numberguess(root)
    root.mainloop()
