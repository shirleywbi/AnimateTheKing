def hex_to_rgb(hex):
    h = hex.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb

def to_greyscale(canvas, item, hex, inc):
    old_rgb = hex_to_rgb(hex)
    max_rgb = max(old_rgb)
    new_rgb = tuple(map(lambda x: x + min(inc, max_rgb - x) if (x < max_rgb) else x, old_rgb))
    new_hex = rgb_to_hex(new_rgb)
    canvas.itemconfig(item, fill=new_hex)