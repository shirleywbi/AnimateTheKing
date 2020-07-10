CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500

IMAGE_WIDTH = 100
IMAGE_OFFSET_X = (CANVAS_WIDTH - IMAGE_WIDTH) / 2
IMAGE_OFFSET_Y = 120
FLOOR = CANVAS_HEIGHT * 0.75

CROWN_HIGH_POINT = IMAGE_OFFSET_Y + 0
CROWN_MID_POINT = IMAGE_OFFSET_Y + 20
CROWN_LOW_POINT = IMAGE_OFFSET_Y + 30
CROWN_HEIGHT = IMAGE_OFFSET_Y + 60
CROWN_SUB_WIDTH = IMAGE_WIDTH / 5

BEARD_THICKNESS = 7
BEARD_COLOR = "#d3d3d3"
BEARD_LENGTH = 100
BEARD_SPACE = CROWN_SUB_WIDTH * 5 / 6 - 2
BEARD_POS_X = IMAGE_OFFSET_X + 3
BEARD_POS_Y = IMAGE_OFFSET_Y + BEARD_LENGTH

BASE_THICKNESS = 50
BASE_COLOR = "maroon"
BASE_SPACE_Y = CROWN_SUB_WIDTH / 2
BASE_POS_X = IMAGE_OFFSET_X
BASE_POS_Y = BEARD_POS_Y + BEARD_LENGTH + BASE_SPACE_Y + BASE_THICKNESS / 2
BASE_WIDTH = CROWN_SUB_WIDTH * 4

# tags
KING = "king"
CROWN = "crown"
BEARD_1 = "beard_1"
BEARD_2 = "beard_2"
BEARD_3 = "beard_3"
BEARD_4 = "beard_4"
BEARD_5 = "beard_5"
BEARD_6 = "beard_6"
BASE = "base"