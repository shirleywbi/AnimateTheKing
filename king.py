import tkinter as tkr
import random
import time
import action_helpers as action
import setup
import util
from constants import *


# Initialize canvas
tk = tkr.Tk()
canvas = tkr.Canvas(tk, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
tk.title("King")
canvas.pack()

beard_list = (BEARD_1, BEARD_2, BEARD_3, BEARD_4, BEARD_5, BEARD_6)
beard_and_base_list = (BEARD_1, BEARD_2, BEARD_3, BEARD_4, BEARD_5, BEARD_6, BASE)

# Initialize images

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

def resize_fire_coords(fire_coords, big_delta, small_delta):
    new_fire_coords = list()
    for i in range(len(fire_coords) - 2):
        if (i % 2 == 1): # Vertical movement
            if i == 15 or i == 17: # Inner base
                new_fire_coords.append(fire_coords[i])
            elif (i < 10): # Upper fire
                new_fire_coords.append(min(fire_coords[i] + random.randint(-big_delta, small_delta), FLOOR))
            elif (i > 10): # Lower fire
                new_fire_coords.append(min(fire_coords[i] + random.randint(-small_delta, small_delta), FLOOR))
        else: # Horizontal movement
            if i == 0: new_fire_coords.append(fire_coords[i] + random.randint(-big_delta, small_delta))
            if i == 2 or i == 4 or i == 6: new_fire_coords.append(fire_coords[i] + random.randint(-small_delta, small_delta))
            if i == 8: new_fire_coords.append(max(fire_coords[i] + random.randint(-small_delta, big_delta), new_fire_coords[6] + 1))
            if i == 10: new_fire_coords.append(max(fire_coords[i] + random.randint(-small_delta, big_delta), fire_coords[14] + 1))
            if i == 12: new_fire_coords.append(max(fire_coords[i] + random.randint(-small_delta, small_delta), fire_coords[14] + 1))
            if i == 14 or i == 16: new_fire_coords.append(fire_coords[i] + random.randint(-small_delta, small_delta))
            if i == 18: new_fire_coords.append(min(fire_coords[i] + random.randint(-small_delta, small_delta), new_fire_coords[16] - 1))
            if i == 20: new_fire_coords.append(min(fire_coords[i] + random.randint(-big_delta, small_delta), new_fire_coords[16] - 1))
    new_fire_coords.append(new_fire_coords[0])
    new_fire_coords.append(new_fire_coords[1])
    return new_fire_coords

def start_fire():

    def get_spark_coords(x_offset, y_offset):
        return [
            x_offset + SPARK_WIDTH / 2, y_offset,
            x_offset, y_offset + SPARK_HEIGHT / 2,
            x_offset + SPARK_WIDTH / 2, y_offset + SPARK_HEIGHT,
            x_offset + SPARK_WIDTH, y_offset + SPARK_HEIGHT / 2,
            x_offset + SPARK_WIDTH / 2, y_offset
        ]

    def create_fire(color, tag):
        old_coords = canvas.coords(CROWN)
        fire_coords = old_coords.copy()
        fire_coords.insert(10, old_coords[8])
        fire_coords.insert(11, (old_coords[9] + old_coords[11])/2)
        fire_coords.insert(14, old_coords[2])
        fire_coords.insert(15, old_coords[11])
        fire_coords.insert(16, old_coords[6])
        fire_coords.insert(17, old_coords[11])
        fire_coords.insert(20, old_coords[0])
        fire_coords.insert(21, fire_coords[11])
        canvas.create_polygon(
            fire_coords,
            fill=color,
            tags=(tag, FIRE)
        )

    def create_spark(x_offset, y_offset, tag):
        canvas.create_polygon(
            get_spark_coords(x_offset, y_offset),
            fill="orange",
            tags=tag
        )

    create_fire("red", FIRE_RED)
    create_fire("orange", FIRE_ORANGE)
    create_fire("gold", FIRE_YELLOW)
    canvas.delete(CROWN)

    i, j, k = 0, -20, -40
    sleep_count = -40
    for count in range(130):
        # Create spark
        if i == 0:
            create_spark(SMOKE_1X, SMOKE_1Y, SPARK_1)
        if j == 0:
            create_spark(SMOKE_2X, SMOKE_2Y, SPARK_2)
        if k == 0:
            create_spark(SMOKE_3X, SMOKE_3Y, SPARK_3)
        # Move spark
        if i >= 0:
            canvas.coords(SPARK_1, get_spark_coords(SMOKE_1X, SMOKE_1Y - i))
        if j >= 0:
            canvas.coords(SPARK_2, get_spark_coords(SMOKE_2X, SMOKE_2Y - j))
        if k >= 0:
            canvas.coords(SPARK_3, get_spark_coords(SMOKE_3X, SMOKE_3Y - k))
        # Remove spark
        if i == 80:
            canvas.delete(SPARK_1)
            i = sleep_count
        if j == 140:
            canvas.delete(SPARK_2)
            j = sleep_count
        if k == 100:
            canvas.delete(SPARK_3)
            k = sleep_count
        # Fire grows
        canvas.coords(FIRE_YELLOW, resize_fire_coords(canvas.coords(FIRE_YELLOW), 2, 2))
        canvas.coords(FIRE_ORANGE, resize_fire_coords(canvas.coords(FIRE_ORANGE), 3, 3))
        canvas.coords(FIRE_RED, resize_fire_coords(canvas.coords(FIRE_RED), 4, 4))
        tk.update()
        time.sleep(0.015)
        i += 1
        j += 1
        k += 1

    canvas.delete(SPARK_1, SPARK_2, SPARK_3)

def shrink_fire():
    for i in range(40):
        canvas.coords(FIRE_YELLOW, resize_fire_coords(canvas.coords(FIRE_YELLOW), 1, 3))
        canvas.coords(FIRE_ORANGE, resize_fire_coords(canvas.coords(FIRE_ORANGE), 2, 4))
        canvas.coords(FIRE_RED, resize_fire_coords(canvas.coords(FIRE_RED), 3, 5))
        tk.update()
        time.sleep(0.02)

def turn_to_ash():

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

    def flatten_item(item, thickness, dec):
        canvas.itemconfig(item, width=thickness - dec)

    i, j, k = 0, -20, -40
    ash_color_inc = 0
    sleep_count = -40
    flatten_count = 0
    while True:
        # Fire turning to ash
        if (ash_color_inc < 30):
            util.to_greyscale(canvas, FIRE_YELLOW, "#FFD700", i * 10)
            util.to_greyscale(canvas, FIRE_ORANGE, "#FFA500", i * 10)
            util.to_greyscale(canvas, FIRE_RED, "#FF0000", i * 10)
        if (ash_color_inc == 30):
            canvas.delete(FIRE)
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
        util.to_greyscale(canvas, BASE, BASE_COLOR, ash_color_inc)
        if (flatten_count < 3):
            flatten_item(BASE, BASE_THICKNESS, 1)
        for beard in beard_list:
            util.to_greyscale(canvas, beard, BEARD_COLOR, ash_color_inc)
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
    time.sleep(0.3)
    collide_crown_with_beard()
    time.sleep(0.1)
    start_fire()
    shrink_fire()
    turn_to_ash()

def restart(event):
    canvas.delete('all')
    setup.setup(canvas)
    animation()

setup.setup(canvas)
tk.bind('<space>', restart)
tk.mainloop()