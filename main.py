import random
import pandas
from tkinter import *

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
# ----------------------READ CSV And Generate Random French Word-----------------------
try:
    data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("./data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=f"{current_card['French']}", fill="black")
    canvas.itemconfig(card, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=f"{current_card['English']}", fill="white")
    canvas.itemconfig(card, image=card_back_img)


def is_known():
    to_learn.remove(current_card)
    data_frame = pandas.DataFrame(to_learn)
    data_frame.to_csv("./data/words_to_learn.csv", index=False)
    next_card()


# ----------------------User Interface-----------------------
window = Tk()
window.title("Flash Card Capstone Project")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# flash card UI
canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
card = canvas.create_image(400, 263, image=card_front_img)
title_text = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# unknown button UI
cross_image = PhotoImage(file="./images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

# known button UI
check_image = PhotoImage(file="./images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

# draw first card
next_card()

window.mainloop()
