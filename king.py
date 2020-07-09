import tkinter as tkr
import random
import time
import action_helpers as action
from constants import *


# Initialize canvas
tk = tkr.Tk()
canvas = tkr.Canvas(tk, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
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

# TODO: Add bounce
def toss_crown(tk, canvas):
    for i in range(10, 0, -1):
        canvas.move(CROWN, 0, -pow(i, 1.5))
        tk.update()
        time.sleep(0.05)

    i = 0
    while (canvas.coords(CROWN)[11] < FLOOR):
        canvas.move(CROWN, 0, min(pow(i, 1.5), FLOOR - canvas.coords(CROWN)[11]))
        tk.update()
        time.sleep(0.05)
        i += 1

def not_on_floor(item):
    return canvas.coords(item)[1] < FLOOR or canvas.coords(item)[3] < FLOOR

def at_least_one_not_on_floor(items):
    for item in items:
        if not_on_floor(item):
            return True
    return False

def collapse_beard(tk, canvas):

    fall_rate = 1.3
    angle_map = { BEARD_1: -.6, BEARD_2: -0.9, BEARD_3: 0.6, BEARD_4: -0.7, BEARD_5: -0.9, BEARD_6: 0.7, BASE: 0.6}
    beard_and_base = (BEARD_1, BEARD_2, BEARD_3, BEARD_4, BEARD_5, BEARD_6, BASE)

    def fall_and_rotate(item):
        if (not_on_floor(item)):
            canvas.move(item, 0, pow(fall_rate, 2))
            action.rotate(canvas, item, angle_map[item])

    while(at_least_one_not_on_floor(beard_and_base)):
        for line in beard_and_base:
            fall_and_rotate(line)
        tk.update()
        time.sleep(0.008)

# Animation
remove_right_foot(tk, canvas)
remove_left_foot(tk, canvas)
beard_into_arms(tk, canvas)
toss_crown(tk, canvas)
collapse_beard(tk, canvas)

tk.mainloop()