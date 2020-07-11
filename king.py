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

beard_list = (BEARD_1, BEARD_2, BEARD_3, BEARD_4, BEARD_5, BEARD_6)
beard_and_base_list = (BEARD_1, BEARD_2, BEARD_3, BEARD_4, BEARD_5, BEARD_6, BASE)

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

def collide_crown_with_beard():
    i = 0
    fall_rate = 3
    angle_map = { BEARD_1: -3, BEARD_2: -4, BEARD_3: 5, BEARD_4: -3.5, BEARD_5: -4.9, BEARD_6: 4.2, BASE: 5.3}
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

def start_fire():

    def expand_fire_coords(fire_coords):
        new_fire_coords = list()
        for i in range(len(fire_coords)):
            if (i == 11 or i == 13):
                new_fire_coords.append(fire_coords[i])
            else:
                new_fire_coords.append(fire_coords[i] + random.randint(-2, 5))
        return new_fire_coords

    def shrink_fire_coords(fire_coords):
        new_fire_coords = list()
        for i in range(len(fire_coords)):
            if (i == 11 or i == 13):
                new_fire_coords.append(fire_coords[i])
            else:
                new_fire_coords.append(fire_coords[i] + random.randint(-5, 2))
        return new_fire_coords

    def get_smoke_coords(x_offset, y_offset):
        return [
            x_offset + SMOKE_WIDTH / 2, y_offset,
            x_offset, y_offset + SMOKE_HEIGHT / 2,
            x_offset + SMOKE_WIDTH / 2, y_offset + SMOKE_HEIGHT,
            x_offset + SMOKE_WIDTH, y_offset + SMOKE_HEIGHT / 2,
            x_offset + SMOKE_WIDTH / 2, y_offset
        ]

    def create_smoke(x_offset, y_offset, tag):
        canvas.create_polygon(
            get_smoke_coords(x_offset, y_offset),
            fill=SMOKE_COLOR,
            tags=tag
        )

    def hex_to_rgb(hex):
        h = hex.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(rgb):
        return "#%02x%02x%02x" % rgb

    def to_greyscale(item, hex, inc):
        old_rgb = hex_to_rgb(hex)
        max_rgb = max(old_rgb)
        new_rgb = tuple(map(lambda x: x + min(inc, max_rgb - x) if (x < max_rgb) else x, old_rgb))
        new_hex = rgb_to_hex(new_rgb)
        canvas.itemconfig(item, fill=new_hex)

    def flatten_item(item, thickness, dec):
        canvas.itemconfig(item, width=thickness - dec)

    canvas.create_polygon(
        canvas.coords(CROWN),
        fill="red",
        tags=FIRE_RED
    )
    canvas.create_polygon(
        canvas.coords(CROWN),
        fill="orange",
        tags=FIRE_ORANGE
    )
    canvas.create_polygon(
        canvas.coords(CROWN),
        fill="gold",
        tags=FIRE_YELLOW
    )
    canvas.delete(CROWN)

    # Grows and burns out
    for i in range(100):
        canvas.coords(FIRE_YELLOW, expand_fire_coords(canvas.coords(FIRE_YELLOW)))
        canvas.coords(FIRE_ORANGE, expand_fire_coords(canvas.coords(FIRE_ORANGE)))
        canvas.coords(FIRE_RED, expand_fire_coords(canvas.coords(FIRE_RED)))
        tk.update()
        time.sleep(0.01)

    for i in range(100):
        canvas.coords(FIRE_YELLOW, shrink_fire_coords(canvas.coords(FIRE_YELLOW)))
        canvas.coords(FIRE_ORANGE, shrink_fire_coords(canvas.coords(FIRE_ORANGE)))
        canvas.coords(FIRE_RED, shrink_fire_coords(canvas.coords(FIRE_RED)))
        tk.update()
        time.sleep(0.01)

    i, j, k = 0, -20, -40
    ash_color_inc = 0
    sleep_count = -40
    flatten_count = 0
    # start_smoking = False
    while True:
        # Create smoke
        if i == 0:
            create_smoke(SMOKE_1X, SMOKE_1Y, SMOKE_1)
        if j == 0:
            create_smoke(SMOKE_2X, SMOKE_2Y, SMOKE_2)
        if k == 0:
            create_smoke(SMOKE_3X, SMOKE_3Y, SMOKE_3)
        # Move smoke
        if i >= 0:
            canvas.coords(SMOKE_1, get_smoke_coords(SMOKE_1X, SMOKE_1Y - i))
        if j >= 0:
            canvas.coords(SMOKE_2, get_smoke_coords(SMOKE_2X, SMOKE_2Y - j))
        if k >= 0:
            canvas.coords(SMOKE_3, get_smoke_coords(SMOKE_3X, SMOKE_3Y - k))
        # Remove smoke
        if i == 80:
            canvas.delete(SMOKE_1)
            i = sleep_count
        if j == 140:
            canvas.delete(SMOKE_2)
            j = sleep_count
        if k == 100:
            canvas.delete(SMOKE_3)
            k = sleep_count
        # Convert to ash
        to_greyscale(BASE, BASE_COLOR, ash_color_inc)
        if (flatten_count < 3):
            flatten_item(BASE, BASE_THICKNESS, 1)
        for beard in beard_list:
            to_greyscale(beard, BEARD_COLOR, ash_color_inc)
            if (flatten_count < 3):
                flatten_item(beard, BEARD_THICKNESS, 1)
        tk.update()
        time.sleep(0.01)
        i += 1
        j += 1
        k += 1
        ash_color_inc += 1
        flatten_count += 1

def animation():
    pick_up_crown_with_beard()
    collide_crown_with_beard()
    start_fire()

def restart(event):
    canvas.delete('all')
    setup()
    animation()

setup()
tk.bind('<space>', restart)
tk.mainloop()