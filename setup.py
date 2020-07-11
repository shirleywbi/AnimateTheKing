from constants import *

def setup(canvas):

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