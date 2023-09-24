from tkinter import *
import pandas
import random
from tkinter import simpledialog, messagebox

word = {}


# --------------------------USER DETAILS ------------------------ #
def user_details():
    user_name = simpledialog.askstring(title="User Details", prompt="Enter Your Name", initialvalue="Guest")
    return user_name


# --------------------------USER INPUT ------------------------ #
username = user_details()


# --------------------------ACCESSING CSV ------------------------ #
try:
    data = pandas.read_csv(f"data/{username}'s_Remaining_Words.csv")
    if data.empty:
        messagebox.showinfo(title="Congratulations", message="You have learned all the words.")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# --------------------------REMAINING WORDS ------------------------ #
def remaining_words():
    to_learn.remove(word)
    remaining = pandas.DataFrame(to_learn)
    remaining.to_csv(f"data/{username}'s_Remaining_Words.csv", index=False)
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

flip_timer = windows.after(3000, func=generate_translation)

canvas = Canvas(width=850, height=550, bg="#B1DDC6", highlightthickness=0)

card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(425, 275, image=card_front)
canvas.grid(column=0, row=0, columnspan=2)

correct_image = PhotoImage(file="images/right.png")
correct_button = Button(image=correct_image, highlightthickness=0, command=remaining_words)
correct_button.grid(column=0, row=1)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=generate_word)
wrong_button.grid(column=1, row=1)

title = canvas.create_text(420, 130, text="", font=("Times", 70, "italic"), fill="#886F6F")

learn_word = canvas.create_text(420, 320, text="", font=("Times", 90, "bold"), fill="#694E4E")

generate_word()
windows.mainloop()
