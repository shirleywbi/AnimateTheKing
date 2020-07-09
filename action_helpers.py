import math

# Formula as per https://math.stackexchange.com/questions/1964905/rotation-around-non-zero-point
def rotate_line_on_pivot(coords, angle):
    return rotate_line_around_point((coords[0], coords[1]), coords, angle)

def rotate_line_around_point(center, coords, angle):
    rad = angle * (math.pi/180)
    cos_val = math.cos(rad)
    sin_val = math.sin(rad)
    x1 = coords[0]
    y1 = coords[1]
    x2 = coords[2]
    y2 = coords[3]
    new_x1 = center[0] + (x1 - center[0]) * cos_val - (y1 - center[1]) * sin_val
    new_y1 = center[1] + (x1 - center[0]) * sin_val + (y1 - center[1]) * cos_val
    new_x2 = center[0] + (x2 - center[0]) * cos_val - (y2 - center[1]) * sin_val
    new_y2 = center[1] + (x2 - center[0]) * sin_val + (y2 - center[1]) * cos_val
    return (new_x1, new_y1, new_x2, new_y2)