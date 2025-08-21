import cv2
import matplotlib.pyplot as plt
import numpy as np
import math

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

img = cv2.imread("datapack/output.png", cv2.IMREAD_COLOR)

colors = ["blue", "green", "red"]

with open('datapack/data/miku/function/build.mcfunction', 'w') as file:
    #file.write(f"setblock ~ ~ ~{i*2} minecraft:barrel[facing=up]{fillTheBarrel(i)}\n")
    pass



