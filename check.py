from tkinter import *
import pandas
import random
from tkinter.simpledialog import askstring

# Function to ask for the user's name
def get_username():
    username = askstring("Username", "Enter your name:")
    return username

# Get the user's name
user_name = get_username()

# Create a user-specific CSV file
user_csv_file = f"data/{user_name}_words.csv"

try:
    data = pandas.read_csv(user_csv_file)
except FileNotFoundError:
    # If the user-specific CSV file doesn't exist, create a new one
    data = pandas.DataFrame(columns=["French", "English"])
    data.to_csv(user_csv_file, index=False)

to_learn = data.to_dict(orient="records")
word = {}
known_words = []

# ... (Rest of your code remains the same) ...
# --------------------------GENERATE FRENCH WORD ------------------------ #
def learned_words():
    global known_words
    known_words.append(word)
    is_known = pandas.DataFrame(known_words)
    to_learn.remove(word)
    is_known.to_csv("data/Learned_Words.csv", index=False)
    generate_word()


# --------------------------GENERATE FRENCH WORD ------------------------ #
def generate_word():
    global word, flip_timer
    windows.after_cancel(flip_timer)
    word = random.choice(to_learn)
    canvas.itemconfig(title, text="French", fill="#886F6F")
    canvas.itemconfig(learn_word, text=word["French"], fill="#694E4E")
    canvas.itemconfig(card_image, image=card_front)
    flip_timer = windows.after(3000, func=generate_translation)


# --------------------------GENERATE ENGLISH TRANSLATION ------------------------ #
def generate_translation():
    canvas.itemconfig(title, text="English", fill="#FFFAF4")
    canvas.itemconfig(learn_word, text=word["English"], fill="white")
    canvas.itemconfig(card_image, image=card_back)


# --------------------------UI SETUP ------------------------ #
windows = Tk()
windows.title("FlashCard Capstone")
windows.config(padx=30, pady=30, bg="#B1DDC6")

# Display the username in the tkinter window
username_label = Label(text=f"Hello, {user_name}!")
username_label.grid(column=0, row=0)

# ... (Rest of your code remains the same) ...
flip_timer = windows.after(3000, func=generate_translation)

canvas = Canvas(width=850, height=550, bg="#B1DDC6", highlightthickness=0)

card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(425, 275, image=card_front)
canvas.grid(column=0, row=0, columnspan=2)

correct_image = PhotoImage(file="images/right.png")
correct_button = Button(image=correct_image, highlightthickness=0, command=learned_words)
correct_button.grid(column=0, row=1)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=generate_word)
wrong_button.grid(column=1, row=1)

title = canvas.create_text(420, 130, text="", font=("Times", 70, "italic"), fill="#886F6F")

learn_word = canvas.create_text(420, 320, text="", font=("Times", 90, "bold"), fill="#694E4E")

generate_word()
windows.mainloop()
