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

    def create_beard(count, tag):
        canvas.create_line(BEARD_POS_X + BEARD_SPACE * count, BEARD_POS_Y, BEARD_POS_X + BEARD_SPACE * count, BEARD_POS_Y + BEARD_LENGTH,
            tags=(tag, KING), width=BEARD_THICKNESS, fill=BEARD_COLOR, cap="round", join="round")

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

    create_beard(0, BEARD_1)
    create_beard(1, BEARD_2)
    create_beard(2, BEARD_3)
    create_beard(3, BEARD_4)
    create_beard(4, BEARD_5)
    create_beard(5, BEARD_6)

    canvas.create_line(BASE_POS_X, BASE_POS_Y, BASE_POS_X + BASE_WIDTH, BASE_POS_Y, tags=(BASE, KING), width=BASE_THICKNESS, fill=BASE_COLOR)
    canvas.tag_lower(BASE)

    canvas.create_line(0, FLOOR, CANVAS_WIDTH, FLOOR, fill="red") # Temporary floor line

# Actions
def beard_into_arms():
    pivot_1 = (canvas.coords(BEARD_1)[0], canvas.coords(BEARD_1)[1])
    pivot_6 = (canvas.coords(BEARD_6)[0], canvas.coords(BEARD_6)[1])
    for i in range(400):
        action.rotate(canvas, BEARD_1, 1, pivot_1)
        action.rotate(canvas, BEARD_6, 1, pivot_6)
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
    beard_into_arms()
    move_crown_up()
    collide_crown_with_beard()

def restart(event):
    canvas.delete('all')
    setup()
    animation()

setup()
tk.bind('<space>', restart)
tk.mainloop()