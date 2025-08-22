import math
import cv2
import numpy as np
import os

nameSpace = "miku"

# Create the necessary directories
dirname = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(dirname, "data", nameSpace, "function"), exist_ok=True)

def items_required(signal_strength, total_slots):
    base = (total_slots * 64) / 14
    requirement = math.ceil(base * (signal_strength - 1))

    return max(signal_strength, requirement)


def fillTheBarrel(signal_strength):
    total_slots = 27
    items_needed = items_required(signal_strength, total_slots)

    output = "{Items:["
    for i in range(items_needed//64):
        output += f"{{Slot:{i}b, count:64, id:\"minecraft:oak_planks\"}},"
    if items_needed % 64 > 0:
        output += f"{{Slot:{items_needed//64}b, count:{items_needed % 64}, id:\"minecraft:oak_planks\"}}"
    output += "]}"

    return output

def image_to_blocks(img, name, pos):
    with open(os.path.join(dirname, "data", nameSpace, "function", f"{name}.mcfunction"), "w") as file:
        for y in range(102):
            for x in range(101):
                if (x + y) % 2 == 1:
                    file.write(
                        f"setblock {pos[0] + x} {pos[1] + y} {pos[2]} minecraft:barrel[facing=north]{fillTheBarrel(int(img[np.clip(99 - y, 0, 99), np.clip(x, 0, 99), 2 - y % 3]//16))}\n")

img = cv2.imread(os.path.join(dirname, "output.png"), cv2.IMREAD_COLOR)
image_to_blocks(img, "image", (155, 76, 152))