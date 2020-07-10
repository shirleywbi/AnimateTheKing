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
def setup():
    canvas.create_polygon(
        IMAGE_OFFSET_X + CROWN_SUB_WIDTH * 0, CROWN_MID_POINT,
        IMAGE_OFFSET_X + CROWN_SUB_WIDTH * 1, CROWN_LOW_POINT,
        IMAGE_OFFSET_X + CROWN_SUB_WIDTH * 2, CROWN_HIGH_POINT,
        IMAGE_OFFSET_X + CROWN_SUB_WIDTH * 3, CROWN_LOW_POINT,
        IMAGE_OFFSET_X + CROWN_SUB_WIDTH * 4, CROWN_MID_POINT,
        IMAGE_OFFSET_X + CROWN_SUB_WIDTH * 4, CROWN_HEIGHT,
        IMAGE_OFFSET_X + CROWN_SUB_WIDTH * 0, CROWN_HEIGHT,
        IMAGE_OFFSET_X + CROWN_SUB_WIDTH * 0, CROWN_MID_POINT,
        fill="gold",
        tags=(CROWN, KING)
    )

    canvas.create_line(BEARD_POS_X + BEARD_SPACE * 0, BEARD_POS_Y, BEARD_POS_X + BEARD_SPACE * 0, BEARD_POS_Y + BEARD_LENGTH, tags=(BEARD_1, KING))
    canvas.create_line(BEARD_POS_X + BEARD_SPACE * 1, BEARD_POS_Y, BEARD_POS_X + BEARD_SPACE * 1, BEARD_POS_Y + BEARD_LENGTH, tags=(BEARD_2, KING))
    canvas.create_line(BEARD_POS_X + BEARD_SPACE * 2, BEARD_POS_Y, BEARD_POS_X + BEARD_SPACE * 2, BEARD_POS_Y + BEARD_LENGTH, tags=(BEARD_3, KING))
    canvas.create_line(BEARD_POS_X + BEARD_SPACE * 3, BEARD_POS_Y, BEARD_POS_X + BEARD_SPACE * 3, BEARD_POS_Y + BEARD_LENGTH, tags=(BEARD_4, KING))
    canvas.create_line(BEARD_POS_X + BEARD_SPACE * 4, BEARD_POS_Y, BEARD_POS_X + BEARD_SPACE * 4, BEARD_POS_Y + BEARD_LENGTH, tags=(BEARD_5, KING))
    canvas.create_line(BEARD_POS_X + BEARD_SPACE * 5, BEARD_POS_Y, BEARD_POS_X + BEARD_SPACE * 5, BEARD_POS_Y + BEARD_LENGTH, tags=(BEARD_6, KING))

    canvas.create_line(BASE_POS_X, BASE_POS_Y, BASE_POS_X + BASE_WIDTH, BASE_POS_Y, tags=(BASE, KING))

    canvas.create_line(LEFT_LEG_POS_X, LEFT_LEG_POS_Y, LEFT_FOOT_POS_X + FOOT_WIDTH, LEFT_FOOT_POS_Y + FOOT_HEIGHT - LEG_LENGTH, tags=(L_LEG, KING))
    canvas.create_oval(LEFT_FOOT_POS_X, LEFT_FOOT_POS_Y, LEFT_FOOT_POS_X + FOOT_WIDTH, LEFT_FOOT_POS_Y + FOOT_HEIGHT, tags=(L_LEG, L_FOOT, KING), fill=FOOT_COLOR)

    canvas.create_line(RIGHT_LEG_POS_X, RIGHT_LEG_POS_Y, RIGHT_FOOT_POS_X, RIGHT_FOOT_POS_Y + FOOT_HEIGHT - LEG_LENGTH, tags=(R_LEG, KING))
    canvas.create_oval(RIGHT_FOOT_POS_X, RIGHT_FOOT_POS_Y, RIGHT_FOOT_POS_X + FOOT_WIDTH, RIGHT_FOOT_POS_Y + FOOT_HEIGHT, tags=(R_LEG, R_FOOT, KING), fill=FOOT_COLOR)

    canvas.create_line(0, FLOOR, CANVAS_WIDTH, FLOOR, fill="red") # Temporary floor line

# Actions
# TODO: Add rotation
def remove_left_foot():
    while (canvas.coords(L_FOOT)[0] <= CANVAS_WIDTH and canvas.coords(L_FOOT)[2] > 0):
        canvas.move(L_LEG, 2, .5)
        tk.update()
        time.sleep(0.01)

# TODO: Add rotation
def remove_right_foot():
    while (canvas.coords(R_FOOT)[0] <= CANVAS_WIDTH and canvas.coords(R_FOOT)[2] > 0):
        canvas.move(R_LEG, 2, -1)
        tk.update()
        time.sleep(0.01)

def beard_into_arms():
    for i in range(400):
        canvas.move(BEARD_1, 2, -1)
        canvas.move(BEARD_6, 2, -1)
        tk.update()
        time.sleep(0.01)

def move_crown_up():
    for i in range(10, 0, -1):
        canvas.move(CROWN, 0, -pow(i, 1.5))
        tk.update()
        time.sleep(0.05)

# TODO: Add crown bounce on floor
# TODO: Add dents
def collide_crown_with_beard():
    i = 0
    fall_rate = 3
    angle_map = { BEARD_1: -3, BEARD_2: -4, BEARD_3: 5, BEARD_4: -3.5, BEARD_5: -4.9, BEARD_6: 4.2, BASE: 5.3}
    beard_and_base = (BEARD_1, BEARD_2, BEARD_3, BEARD_4, BEARD_5, BEARD_6, BASE)
    drop_beard = False

    def fall_and_rotate(item):
        if (not_on_floor(item)):
            canvas.move(item, 0, pow(fall_rate, 2))
            action.rotate(canvas, item, angle_map[item])

    def not_on_floor(item):
        return canvas.coords(item)[1] < FLOOR or canvas.coords(item)[3] < FLOOR

    def at_least_one_not_on_floor(items):
        for item in items:
            if not_on_floor(item):
                return True
        return False

    def collapse_beard():
        if (at_least_one_not_on_floor(beard_and_base)):
            for line in beard_and_base:
                fall_and_rotate(line)

    def pause_on_impact():
        if (not drop_beard):
            time.sleep(0.01)

    while (canvas.coords(CROWN)[11] < FLOOR or at_least_one_not_on_floor(beard_and_base)):
        if canvas.coords(CROWN)[11] < FLOOR:
            canvas.move(CROWN, 0, min(pow(i, 1.2), FLOOR - canvas.coords(CROWN)[11]))
        if canvas.coords(CROWN)[11] > canvas.coords(BEARD_1)[1]:
            pause_on_impact()
            drop_beard = True
        if drop_beard:
            collapse_beard()
        tk.update()
        time.sleep(0.01)
        i += 0.1

def animation():
    # remove_right_foot()
    # remove_left_foot()
    #beard_into_arms()
    move_crown_up()
    collide_crown_with_beard()

def restart(event):
    canvas.delete('all')
    setup()
    animation()

setup()
tk.bind('<space>', restart)
tk.mainloop()