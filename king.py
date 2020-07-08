from tkinter import *
import random
import time
from constants import *


# Initialize canvas
tk = Tk()
canvas = Canvas(tk, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
tk.title("King")
canvas.pack()

# Initialize images
crown = canvas.create_polygon(
    IMAGE_OFFSET_X + CROWN_SUB_WIDTH * 0, CROWN_MID_POINT,
    IMAGE_OFFSET_X + CROWN_SUB_WIDTH * 1, CROWN_LOW_POINT,
    IMAGE_OFFSET_X + CROWN_SUB_WIDTH * 2, CROWN_HIGH_POINT,
    IMAGE_OFFSET_X + CROWN_SUB_WIDTH * 3, CROWN_LOW_POINT,
    IMAGE_OFFSET_X + CROWN_SUB_WIDTH * 4, CROWN_MID_POINT,
    IMAGE_OFFSET_X + CROWN_SUB_WIDTH * 4, CROWN_HEIGHT,
    IMAGE_OFFSET_X + CROWN_SUB_WIDTH * 0, CROWN_HEIGHT,
    IMAGE_OFFSET_X + CROWN_SUB_WIDTH * 0, CROWN_MID_POINT,
    fill="gold",
    tags=CROWN
)

beard_1 = canvas.create_line(BEARD_POS_X + BEARD_SPACE * 0, BEARD_POS_Y, BEARD_POS_X + BEARD_SPACE * 0, BEARD_POS_Y + BEARD_LENGTH, tags=BEARD_1)
beard_2 = canvas.create_line(BEARD_POS_X + BEARD_SPACE * 1, BEARD_POS_Y, BEARD_POS_X + BEARD_SPACE * 1, BEARD_POS_Y + BEARD_LENGTH, tags=BEARD_2)
beard_3 = canvas.create_line(BEARD_POS_X + BEARD_SPACE * 2, BEARD_POS_Y, BEARD_POS_X + BEARD_SPACE * 2, BEARD_POS_Y + BEARD_LENGTH, tags=BEARD_3)
beard_4 = canvas.create_line(BEARD_POS_X + BEARD_SPACE * 3, BEARD_POS_Y, BEARD_POS_X + BEARD_SPACE * 3, BEARD_POS_Y + BEARD_LENGTH, tags=BEARD_4)
beard_5 = canvas.create_line(BEARD_POS_X + BEARD_SPACE * 4, BEARD_POS_Y, BEARD_POS_X + BEARD_SPACE * 4, BEARD_POS_Y + BEARD_LENGTH, tags=BEARD_5)
beard_6 = canvas.create_line(BEARD_POS_X + BEARD_SPACE * 5, BEARD_POS_Y, BEARD_POS_X + BEARD_SPACE * 5, BEARD_POS_Y + BEARD_LENGTH, tags=BEARD_6)

base = canvas.create_line(BASE_POS_X, BASE_POS_Y, BASE_POS_X + BASE_WIDTH, BASE_POS_Y, tags=BASE)

canvas.create_line(LEFT_LEG_POS_X, LEFT_LEG_POS_Y, LEFT_FOOT_POS_X + FOOT_WIDTH, LEFT_FOOT_POS_Y + FOOT_HEIGHT - LEG_LENGTH, tags=L_LEG)
canvas.create_oval(LEFT_FOOT_POS_X, LEFT_FOOT_POS_Y, LEFT_FOOT_POS_X + FOOT_WIDTH, LEFT_FOOT_POS_Y + FOOT_HEIGHT, tags=(L_LEG, L_FOOT), fill=FOOT_COLOR)

canvas.create_line(RIGHT_LEG_POS_X, RIGHT_LEG_POS_Y, RIGHT_FOOT_POS_X, RIGHT_FOOT_POS_Y + FOOT_HEIGHT - LEG_LENGTH, tags=R_LEG)
canvas.create_oval(RIGHT_FOOT_POS_X, RIGHT_FOOT_POS_Y, RIGHT_FOOT_POS_X + FOOT_WIDTH, RIGHT_FOOT_POS_Y + FOOT_HEIGHT, tags=(R_LEG, R_FOOT), fill=FOOT_COLOR)

# Actions
# TODO: Add rotation
def remove_left_foot(tk, canvas):
    while (canvas.coords(L_FOOT)[0] <= CANVAS_WIDTH and canvas.coords(L_FOOT)[2] > 0):
        canvas.move(L_LEG, 2, .5)
        tk.update()
        time.sleep(0.01)

# TODO: Add rotation
def remove_right_foot(tk, canvas):
    while (canvas.coords(R_FOOT)[0] <= CANVAS_WIDTH and canvas.coords(R_FOOT)[2] > 0):
        canvas.move(R_LEG, 2, -1)
        tk.update()
        time.sleep(0.01)

def beard_into_arms(tk, canvas):
    for i in range(400):
        canvas.move(BEARD_1, 2, -1)
        canvas.move(BEARD_6, 2, -1)
        tk.update()
        time.sleep(0.01)

# TODO: Add bounce, fix disappearing crown
def toss_crown(tk, canvas):
    for i in range(9, 0, -1):
        canvas.move(CROWN, 0, -pow(i, 2))
        tk.update()
        time.sleep(0.05)

    i = 0
    while (canvas.coords(CROWN)[3] < FLOOR):
        canvas.move(CROWN, 0, max(pow(i, 2), FLOOR))
        tk.update()
        time.sleep(0.05)
        i += 1

def collapse_beard(tk, canvas):
    while (
        canvas.coords(BEARD_1)[3] < FLOOR or
        canvas.coords(BEARD_2)[3] < FLOOR or
        canvas.coords(BEARD_3)[3] < FLOOR or
        canvas.coords(BEARD_4)[3] < FLOOR or
        canvas.coords(BEARD_5)[3] < FLOOR or
        canvas.coords(BEARD_6)[3] < FLOOR or
        canvas.coords(BASE)[3] < FLOOR):
        canvas.move(BEARD_1, 0, min(1, canvas.coords(BEARD_1)[3] < FLOOR))
        canvas.move(BEARD_2, 0, min(1, canvas.coords(BEARD_2)[3] < FLOOR))
        canvas.move(BEARD_3, 0, min(1, canvas.coords(BEARD_3)[3] < FLOOR))
        canvas.move(BEARD_4, 0, min(1, canvas.coords(BEARD_4)[3] < FLOOR))
        canvas.move(BEARD_5, 0, min(1, canvas.coords(BEARD_5)[3] < FLOOR))
        canvas.move(BEARD_6, 0, min(1, canvas.coords(BEARD_6)[3] < FLOOR))
        canvas.move(BASE, 0, min(1, canvas.coords(BASE)[3] < FLOOR))
        tk.update()
        time.sleep(0.01)

# Animation
remove_right_foot(tk, canvas)
remove_left_foot(tk, canvas)
beard_into_arms(tk, canvas)
toss_crown(tk, canvas)
collapse_beard(tk, canvas)

tk.mainloop()