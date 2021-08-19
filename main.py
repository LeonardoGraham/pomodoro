from tkinter import * \
    # ---------------------------- CONSTANTS ------------------------------- #

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
CHECK_MARK = "✔"
SECS_IN_MIN = 60
MILLI_SECS_IN_SEC = 1000  # Default = 1000
WORK_MIN = 25  # Default = 25
SHORT_BREAK_MIN = 5  # Default = 5
LONG_BREAK_MIN = 20  # Default = 20

reps = 0
check_marks_count = ''
timer = None


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    start_button.config(state="normal")
    reset_button.config(state="disabled")

    global reps
    global check_marks_count

    check_marks_count = ''
    reps = 0

    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer", fg=GREEN)

    check_marks_label.config(text=check_marks_count)


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    start_button.config(state="disabled")
    reset_button.config(state="normal")

    global reps
    reps += 1

    work_secs = WORK_MIN * SECS_IN_MIN
    short_break_secs = SHORT_BREAK_MIN * SECS_IN_MIN
    long_break_secs = LONG_BREAK_MIN * SECS_IN_MIN

    if reps % 2 == 0:
        if reps % 8 == 0:
            title_label.config(text="Break", fg=RED)
            count_down(long_break_secs)
        else:
            title_label.config(text="Break", fg=PINK)
            count_down(short_break_secs)
    else:
        title_label.config(text="Work", fg=GREEN)
        count_down(work_secs)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global reps
    global check_marks_count

    count_min = count // SECS_IN_MIN
    count_sec = count % SECS_IN_MIN

    canvas.itemconfig(timer_text, text=f"{count_min:02d}:{count_sec:02d}")
    if count > 0:
        global timer
        timer = window.after(MILLI_SECS_IN_SEC, count_down, count - 1)
    else:
        window.lift()
        window.attributes('-topmost', True)
        window.after_idle(window.attributes, '-topmost', False)

        start_timer()
        if reps % 8 == 1:
            check_marks_count = ''
        elif reps % 2 == 0:
            check_marks_count += CHECK_MARK

        check_marks_label.config(text=check_marks_count)


# ---------------------------- UI SETUP ------------------------------- #
# Window
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

# Canvas
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 135, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

# Label
title_label = Label(text="Timer", font=(FONT_NAME, 35, "bold"), bg=YELLOW, fg=GREEN)
title_label.grid(row=0, column=1)

check_marks_label = Label(font=(FONT_NAME, 20), bg=YELLOW, fg=GREEN)
check_marks_label.grid(row=3, column=1)

# Buttons
start_button = Button(text="Start", highlightthickness=0, command=start_timer, state="normal")
start_button.grid(row=2, column=0)

reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer, state="disabled")
reset_button.grid(row=2, column=2)

window.mainloop()
