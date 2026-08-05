from tkinter import *
from PIL import ImageTk, Image
from wordfreq import top_n_list
import random
import time

TOTAL_SECONDS = 60
TIMER_STARTED = False
CURRENT_INDEX = 0
CURRENT_WORDS = []
WORD_POSITIONS = []

CORRECT_WORDS = 0
WRONG_WORDS = 0
TOTAL_TYPED = 0
CORRECT_CHARACTERS = 0

def welcome_screen():
    canvas.itemconfig(card_title, text="Welcome to\nTypeSpeed\nChecker!")
    canvas.itemconfig(card_text, text="Press the button to start")
    start_btn.place(x=500, y=550, anchor=CENTER)

    restart_btn.place_forget()
    timer.place_forget()
    words_box.place_forget()
    text_box.place_forget()

def start():
    canvas.itemconfig(card_title, text="")
    canvas.itemconfig(card_text, text="")
    start_btn.place_forget()

    restart_btn.place(x=500, y=665, anchor=CENTER)
    timer.place(x=800, y=120, anchor=CENTER)
    text_box.place(x=500, y=500, anchor=CENTER)
    words_box.place(x=500, y=260, anchor=CENTER)

    generate_words()


def restart():
    global TOTAL_SECONDS, TIMER_STARTED, CURRENT_INDEX, CURRENT_WORDS, WORD_POSITIONS
    global CORRECT_WORDS, WRONG_WORDS, TOTAL_TYPED, CORRECT_CHARACTERS

    TOTAL_SECONDS = 60
    TIMER_STARTED = False

    CURRENT_INDEX = 0
    CURRENT_WORDS.clear()
    WORD_POSITIONS.clear()

    CORRECT_WORDS = 0
    WRONG_WORDS = 0
    TOTAL_TYPED = 0
    CORRECT_CHARACTERS = 0

    timer.config(text="01:00")

    text_box.config(state="normal")
    text_box.delete("1.0", END)

    words_box.config(state="normal")
    words_box.delete("1.0", END)
    words_box.tag_remove("correct", "1.0", END)
    words_box.tag_remove("wrong", "1.0", END)
    words_box.tag_remove("current", "1.0", END)
    words_box.config(state="disabled")

    welcome_screen()

def countdown_timer():
    global TOTAL_SECONDS

    minutes, seconds = divmod(TOTAL_SECONDS, 60)
    time_format = f"{minutes:02d}:{seconds:02d}"
    timer.config(text=time_format, background="#eeeeee", font=("Courier", 19, "bold"), fg="black")

    if TOTAL_SECONDS > 0:
        TOTAL_SECONDS -= 1
        window.after(1000, countdown_timer)
    elif TOTAL_SECONDS == 0:
        calculate_wpm()
        words_box.place_forget()
        text_box.config(state="disabled")

def first_key_pressed(event):
    global TIMER_STARTED
    if not TIMER_STARTED:
        TIMER_STARTED = True
        countdown_timer()

def generate_words():
    global CURRENT_INDEX, CURRENT_WORDS, WORD_POSITIONS

    words = [
        word
        for word in top_n_list("en", 10000)
    ]

    CURRENT_INDEX = 0
    CURRENT_WORDS = random.sample(words, 30)

    WORD_POSITIONS.clear()

    words_box.config(state="normal")
    words_box.delete("1.0", END)

    for word in CURRENT_WORDS:

        word_start = words_box.index("end-1c")

        words_box.insert(END, word + " ")

        word_end = f"{word_start}+{len(word)}c"

        WORD_POSITIONS.append((word_start, word_end))

    words_box.tag_remove("correct", "1.0", END)
    words_box.tag_remove("wrong", "1.0", END)
    words_box.tag_remove("current", "1.0", END)

    first_start, first_end = WORD_POSITIONS[0]
    words_box.tag_add("current", first_start, first_end)

    words_box.config(state="disabled")

def check_word(event):
    global CURRENT_INDEX, CORRECT_WORDS, WRONG_WORDS, TOTAL_TYPED, CORRECT_CHARACTERS

    typed_words = text_box.get("1.0", "end-1c").split()

    if len(typed_words) <= CURRENT_INDEX:
        return

    typed = typed_words[CURRENT_INDEX]

    word_start, word_end = WORD_POSITIONS[CURRENT_INDEX]

    words_box.config(state="normal")

    # remove highlight from current word
    words_box.tag_remove("current", word_start, word_end)

    if typed == CURRENT_WORDS[CURRENT_INDEX]:
        words_box.tag_add("correct", word_start, word_end)
        CORRECT_WORDS += 1
        TOTAL_TYPED += 1
        CORRECT_CHARACTERS += len(typed)
    else:
        words_box.tag_add("wrong", word_start, word_end)
        WRONG_WORDS += 1
        TOTAL_TYPED += 1

    CURRENT_INDEX += 1

    # Finished current batch?
    if CURRENT_INDEX == len(CURRENT_WORDS):
        generate_words()
        text_box.delete("1.0", END)
    else:
        next_start, next_end = WORD_POSITIONS[CURRENT_INDEX]
        words_box.tag_add("current", next_start, next_end)

    words_box.config(state="disabled")

def calculate_wpm():
    global TOTAL_TYPED, CORRECT_CHARACTERS
    accuracy = round((CORRECT_WORDS / TOTAL_TYPED) * 100)
    wpm = round((CORRECT_CHARACTERS / 5))
    words_box.place_forget()
    canvas.itemconfig(
        card_title,
        text=f"           WPM : {wpm}              \n           Accuracy : {accuracy}%           ",
        font=("Courier", 70, "bold"),
    )




#------------------------------------------------- UI SETUP -------------------------------------------------
window = Tk()
window.title("Typing Speed Checker")
window.config(padx=10, pady=10)

canvas = Canvas(bg="#FAA0A0", width=1000, height=800 )
img = Image.open("images/card.png")
card_img = ImageTk.PhotoImage(img)
card = canvas.create_image(500, 400, image=card_img)
card_title = canvas.create_text(500, 250, text="", font=("Courier", 50, "bold"), fill="black")
card_text = canvas.create_text(500, 425, text="", font=("Courier", 30, "italic"), fill="black")
canvas.pack()

start_img = PhotoImage(file="images/start.png")
start_btn = Button(image=start_img, highlightthickness=0, height=130, width=256, bd=0, command=start)


restart_img = PhotoImage(file="images/restart.png")
restart_btn = Button(image=restart_img, highlightthickness=0, height=100, width=110, bd=0, command=restart)
restart_btn.place_forget()

timer = Label(text="01:00", background="#eeeeee", font=("Courier", 19, "bold"), fg="black")
timer.place_forget()

words_box = Text(
        width=45,
        height=7,
        font=("Courier", 20, "bold"),
        bd=0,
        highlightthickness=0,
        wrap="word",
        bg="#eeeeee",
        foreground="black",
    )

words_box.place_forget()
words_box.tag_config("correct", foreground="#2e7d32")
words_box.tag_config("wrong", foreground="#d32f2f")
words_box.tag_config("current", background="#cfcfcf")
words_box.config(state="disabled")

text_box = Text(font=("Courier", 20, "bold"), highlightthickness=0, width=45, height=7)
text_box.place_forget()

text_box.bind("<Key>", first_key_pressed)
text_box.bind("<space>", check_word)

welcome_screen()


window.mainloop()