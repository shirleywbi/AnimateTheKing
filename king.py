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

    def create_beard_arm(count, tag):
        x = BEARD_POS_X + BEARD_SPACE * count
        canvas.create_line(x, BEARD_POS_Y, x, BEARD_POS_Y + BEARD_LENGTH / 2, x, BEARD_POS_Y + BEARD_LENGTH,
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

    create_beard_arm(0, BEARD_1)
    create_beard(1, BEARD_2)
    create_beard(2, BEARD_3)
    create_beard(3, BEARD_4)
    create_beard(4, BEARD_5)
    create_beard_arm(5, BEARD_6)

    canvas.create_line(BASE_POS_X, BASE_POS_Y, BASE_POS_X + BASE_WIDTH, BASE_POS_Y, tags=(BASE, KING), width=BASE_THICKNESS, fill=BASE_COLOR)
    canvas.tag_lower(BASE)

# Actions
def pick_up_crown_with_beard():

    left_arm = canvas.coords(BEARD_1)
    left_shoulder = (left_arm[0], left_arm[1])
    left_elbow = ((left_arm[2] + left_arm[0])/2, (left_arm[3] + left_arm[1])/2)
    left_hand = (left_arm[2], left_arm[3])

    right_arm = canvas.coords(BEARD_6)
    right_shoulder = (right_arm[0], right_arm[1])
    right_elbow = ((right_arm[2] + right_arm[0])/2, (right_arm[3] + right_arm[1])/2)
    right_hand = (right_arm[2], right_arm[3])

    def is_touching_crown():
        right_x = canvas.coords(BEARD_1)[4] <= canvas.coords(CROWN)[8] and canvas.coords(BEARD_1)[4] >= canvas.coords(CROWN)[0]
        right_y = canvas.coords(BEARD_1)[5] <= canvas.coords(CROWN)[11] and canvas.coords(BEARD_1)[5] >= canvas.coords(CROWN)[9]
        return right_x and right_y

    def is_elbow_above_shoulder():
        return canvas.coords(BEARD_1)[0] <= canvas.coords(BEARD_1)[2] + 1

    def is_arm_extended():
        return is_elbow_above_shoulder() and canvas.coords(BEARD_1)[1] - canvas.coords(BEARD_1)[5] == BEARD_LENGTH

    # Grab crown
    i = 0
    while (not is_touching_crown()):
        canvas.coords(BEARD_1, left_shoulder[0], left_shoulder[1], left_elbow[0] - i/4, left_elbow[1] - i/4, left_hand[0], left_hand[1] - i)
        canvas.coords(BEARD_6, right_shoulder[0], right_shoulder[1], right_elbow[0] + i/4, right_elbow[1] - i/4, right_hand[0], right_hand[1] - i)
        tk.update()
        time.sleep(0.008)
        i += 1

    # Straighten arms
    j = 0
    while (not is_elbow_above_shoulder()):
        canvas.coords(BEARD_1, left_shoulder[0], left_shoulder[1], left_elbow[0] - i/4 + j, left_elbow[1] - i/4 - j, left_hand[0], left_hand[1] - i - j)
        canvas.coords(BEARD_6, right_shoulder[0], right_shoulder[1], right_elbow[0] + i/4 - j, right_elbow[1] - i/4 - j, right_hand[0], right_hand[1] - i - j)
        tk.update()
        time.sleep(0.008)
        j += 1

    # Lengthen arms and pick up crown
    k = 0
    k_rate = 1
    crown_coords = canvas.coords(CROWN)
    while (not is_arm_extended()):
        for c in range(len(crown_coords)):
            if c % 2 != 0:
                crown_coords[c] -= k_rate

        canvas.coords(BEARD_1, left_shoulder[0], left_shoulder[1], left_elbow[0] - i/4 + j, left_elbow[1] - i/4 - j, left_hand[0], left_hand[1] - i - j - k)
        canvas.coords(BEARD_6, right_shoulder[0], right_shoulder[1], right_elbow[0] + i/4 - j, right_elbow[1] - i/4 - j, right_hand[0], right_hand[1] - i - j - k)
        canvas.coords(CROWN, crown_coords)
        tk.update()
        time.sleep(0.01)
        k += k_rate

    canvas.coords(BEARD_1, left_shoulder[0], left_shoulder[1], left_hand[0], left_hand[1] - i - j - k)
    canvas.coords(BEARD_6, right_shoulder[0], right_shoulder[1], right_hand[0], right_hand[1] - i - j - k)
    time.sleep(1)

# TODO: Add crown bounce on floor
# TODO: Add dents
def collide_crown_with_beard():
    i = 0
    fall_rate = 3
    angle_map = { BEARD_1: -3, BEARD_2: -4, BEARD_3: 5, BEARD_4: -3.5, BEARD_5: -4.9, BEARD_6: 4.2, BASE: 5.3}
    beard_list = (BEARD_1, BEARD_2, BEARD_3, BEARD_4, BEARD_5, BEARD_6)
    beard_and_base_list = (BEARD_1, BEARD_2, BEARD_3, BEARD_4, BEARD_5, BEARD_6, BASE)
    drop_beard = False
    drop_base = False

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
        if (at_least_one_not_on_floor(beard_list)):
            for line in beard_list:
                fall_and_rotate(line)

    def collapse_base():
        if (not_on_floor(BASE)):
            fall_and_rotate(BASE)

    while (canvas.coords(CROWN)[11] < FLOOR or at_least_one_not_on_floor(beard_and_base_list)):
        if canvas.coords(CROWN)[11] < FLOOR:
            canvas.move(CROWN, 0, min(pow(i, 2), FLOOR - canvas.coords(CROWN)[11]))
        if canvas.coords(CROWN)[11] > canvas.coords(BEARD_1)[1]:
            drop_beard = True
        if canvas.coords(CROWN)[11] > canvas.coords(BASE)[1]:
            drop_base = True
        if drop_beard:
            collapse_beard()
        if drop_base:
            collapse_base()
        tk.update()
        time.sleep(0.015)
        i += 0.05

def animation():
    pick_up_crown_with_beard()
    collide_crown_with_beard()

def restart(event):
    canvas.delete('all')
    setup()
    animation()

setup()
tk.bind('<space>', restart)
tk.mainloop()