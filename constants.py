CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500

IMAGE_WIDTH = 100
IMAGE_OFFSET_X = (CANVAS_WIDTH - IMAGE_WIDTH) / 2
IMAGE_OFFSET_Y = 120

CROWN_HIGH_POINT = IMAGE_OFFSET_Y + 0
CROWN_MID_POINT = IMAGE_OFFSET_Y + 20
CROWN_LOW_POINT = IMAGE_OFFSET_Y + 30
CROWN_HEIGHT = IMAGE_OFFSET_Y + 60
CROWN_SUB_WIDTH = IMAGE_WIDTH / 5

BEARD_POS_X = IMAGE_OFFSET_X + 0
BEARD_POS_Y = IMAGE_OFFSET_Y + 100
BEARD_LENGTH = 100
BEARD_SPACE = CROWN_SUB_WIDTH * 5 / 6

BASE_SPACE_Y = CROWN_SUB_WIDTH
BASE_POS_X = BEARD_POS_X
BASE_POS_Y = BEARD_POS_Y + BEARD_LENGTH + BASE_SPACE_Y
BASE_WIDTH = CROWN_SUB_WIDTH * 4.1

LEG_LENGTH = 30
LEG_GAP = CROWN_SUB_WIDTH * 2
FOOT_COLOR = "grey"
FOOT_SPACE_Y = 0
FOOT_WIDTH = CROWN_SUB_WIDTH * 1.5
FOOT_HEIGHT = CROWN_SUB_WIDTH * 2/3

LEFT_FOOT_POS_X = IMAGE_OFFSET_X - (CROWN_SUB_WIDTH / 2)
LEFT_FOOT_POS_Y = BASE_POS_Y + FOOT_SPACE_Y + LEG_LENGTH
LEFT_LEG_POS_X = LEFT_FOOT_POS_X + FOOT_WIDTH
LEFT_LEG_POS_Y = LEFT_FOOT_POS_Y + (FOOT_HEIGHT / 2)

RIGHT_FOOT_POS_X = LEFT_LEG_POS_X + LEG_GAP
RIGHT_FOOT_POS_Y = LEFT_FOOT_POS_Y
RIGHT_LEG_POS_X = RIGHT_FOOT_POS_X
RIGHT_LEG_POS_Y = RIGHT_FOOT_POS_Y + (FOOT_HEIGHT / 2)

# tags
CROWN = "crown"
BEARD_1 = "beard_1"
BEARD_2 = "beard_2"
BEARD_3 = "beard_3"
BEARD_4 = "beard_4"
BEARD_5 = "beard_5"
BEARD_6 = "beard_6"
BASE = "base"
L_FOOT = "left_foot"
R_FOOT = "right_foot"