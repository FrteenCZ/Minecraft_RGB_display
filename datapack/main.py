import math
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

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
        for y in range(img.shape[0] + 2):
            for x in range(img.shape[1] + 1):
                if (x + y) % 2 == 1:
                    file.write(
                        f"setblock {pos[0] + x} {pos[1] + y} {pos[2]} minecraft:barrel[facing=north]{fillTheBarrel(int(img[np.clip(99 - y, 0, 99), np.clip(x, 0, 99), 2 - y % 3]//16))}\n")


def process_image(img, width=100, height=100):
    img = cv2.resize(img, (width, height))
    output = np.zeros_like(img, dtype=np.uint8)

    for y in range(-1, height + 1):
        for x in range(-1, width):
            if (y + x) % 2 == 0:

                y0 = np.clip(y - 1, 0, height)
                y1 = np.clip(y + 2, 0, height)
                x0 = np.clip(x, 0, width)
                x1 = np.clip(x + 2, 0, width)

                c = (y + 1) % 3
                output[y0:y1, x0:x1, c] = np.average(img[y0:y1, x0:x1, c])

    return output



input_image_paths = os.listdir(os.path.join(dirname, "input_images"))
input_image_paths = [f for f in input_image_paths if f.endswith(".png")] # Filter only .png files


figure, axes = plt.subplots(1, len(input_image_paths), figsize=(4*len(input_image_paths), 4))

# If there's only one image, wrap axes in a list for consistency
if len(input_image_paths) == 1:
    axes = [axes]

for i, path in enumerate(input_image_paths):
    img = cv2.imread(os.path.join(dirname, "input_images", path), cv2.IMREAD_COLOR)
    img = process_image(img)
    image_to_blocks(img, os.path.splitext(path)[0], (155, 76, 152))

    axes[i].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    axes[i].set_title(os.path.splitext(path)[0])
    axes[i].axis("off")

    plt.pause(0.5)  # short pause so the figure updates

plt.show()