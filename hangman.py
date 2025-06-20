import tkinter as tk
import random
from functools import partial

# Word list
words_by_category = {
    "Fruits": ['apple', 'grape', 'olive', 'melon', 'dates', 'aarza', 'peach', 'areca', 'berry', 'kepel', 'mango', 'pluot', 'guava']
}

# Game state
category = "Fruits"
secret_word = random.choice(words_by_category[category]).lower()
guessed_letters = set()
max_attempts = 6
wrong_attempts = 0

# ---- Functions ---- #

def update_display():
    display_word = " ".join([letter if letter in guessed_letters else "_" for letter in secret_word])
    word_label.config(text=display_word)

def letter_pressed(letter, button):
    global wrong_attempts

    if letter in guessed_letters or wrong_attempts >= max_attempts:
        return

    guessed_letters.add(letter)

    if letter in secret_word:
        update_display()
        if all(l in guessed_letters for l in secret_word):
            status_label.config(text="🎉 You guessed the word!")
            disable_all_buttons()
            keyboard_frame.pack_forget()  # Hide keyboard
            show_win_animation()
    else:
        button.config(text=f"{letter} ❌", state="disabled")
        wrong_attempts += 1
        if wrong_attempts >= max_attempts:
            status_label.config(text=f"😢 Out of attempts! Word was '{secret_word}'")
            disable_all_buttons()
            keyboard_frame.pack_forget()  # Hide keyboard
            show_loss_animation()

def disable_all_buttons():
    for btn in letter_buttons:
        btn.config(state="disabled")

def enable_all_buttons():
    for i, btn in enumerate(letter_buttons):
        btn.config(state="normal", text=alphabet[i])

def play_again():
    global secret_word, guessed_letters, wrong_attempts
    secret_word = random.choice(words_by_category[category]).lower()
    guessed_letters = set()
    wrong_attempts = 0
    update_display()
    enable_all_buttons()
    status_label.config(text="")
    animation_label.config(text="", bg=window.cget("bg"))  # Reset color
    keyboard_frame.pack()  # Show keyboard again
    play_again_btn.pack_forget()

# 🎉 Win Animation
def show_win_animation():
    frames = ["🎇🎉😄🎉🎇", "✨💥😄💥✨", "🎆🥳😄🥳🎆", "💫🎉😄🎉💫"]
    colors = ["#FFDD00", "#FF61A6", "#7FFFD4", "#FF6347"]
    
    def animate(index=0):
        if index < len(frames):
            animation_label.config(text=frames[index], bg=colors[index % len(colors)])
            window.after(500, animate, index + 1)
        else:
            animation_label.config(text="🎉 You Win! 😄", bg="#98FB98")  # Final frame
            play_again_btn.pack(pady=10)

    animate()

# 😢 Lose Animation
def show_loss_animation():
    frames = ["😢", "😢", "💔 Try Again 💔", "😭", "😢 Try Again 😢"]
    colors = ["#F08080", "#FA8072", "#FF7F7F", "#CD5C5C"]
    
    def animate(index=0):
        if index < len(frames):
            animation_label.config(text=frames[index], bg=colors[index % len(colors)])
            window.after(500, animate, index + 1)
        else:
            animation_label.config(text="😢 Try Again!", bg="#FFB6C1")
            play_again_btn.pack(pady=10)

    animate()

# ---- GUI Setup ---- #

window = tk.Tk()
window.title("Guess the Word - Hangman")
window.geometry("600x500")
window.resizable(False, False)

# Category Title
tk.Label(window, text=category, font=("Arial", 18, "bold"), borderwidth=2,
         relief="groove", padx=10, pady=5).pack(pady=10)

# Word display
word_label = tk.Label(window, text="_ " * len(secret_word), font=("Courier", 32))
word_label.pack(pady=20)

# Keyboard frame
keyboard_frame = tk.Frame(window)
keyboard_frame.pack()

letter_buttons = []
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
row = 0
col = 0

for i, letter in enumerate(alphabet):
    btn = tk.Button(keyboard_frame, text=letter, width=4, font=("Arial", 14),
                    command=partial(letter_pressed, letter.lower(), None))
    btn.grid(row=row, column=col, padx=3, pady=3)
    letter_buttons.append(btn)
    col += 1
    if (i + 1) % 9 == 0:
        row += 1
        col = 0

# Assign buttons their command
for i, btn in enumerate(letter_buttons):
    letter = alphabet[i].lower()
    btn.config(command=partial(letter_pressed, letter, btn))

# Status message
status_label = tk.Label(window, text="", font=("Arial", 12), fg="blue")
status_label.pack(pady=10)

# Animation label
animation_label = tk.Label(window, text="", font=("Arial", 36), width=25, height=2)
animation_label.pack(pady=10)

# Play Again Button (initially hidden)
play_again_btn = tk.Button(window, text="🔁 Play Again", font=("Arial", 12, "bold"),
                           bg="green", fg="white", command=play_again)

# Main loop
window.mainloop()
