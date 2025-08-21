import json
import cv2
import numpy as np

sides = ["west", "north", "east", "south"]
colors = ["blue", "green", "red"]

color_combos = {
    "blue": ["north", "side"],
    "green": ["south", "side"],
    "red": ["north", "up"]
}


texture_size = 9

# --- blockstates ---
multipart = []
for color in colors:
    print(f"Generating blockstates for {color}")
    for power in range(16):
        part = {"when": {},
                "apply": {}}

        for side in sides:
            part["when"][side] = "none"

        part["when"]["power"] = power
        part["when"][color_combos[color][0]] = color_combos[color][1]

        part["apply"]["model"] = f"block/{color}_{power}"

        multipart.append(part)

# Add the default part
# IDC that this is not pretty, it works :P
output = json.dumps({"multipart": multipart})
output = output[:-2] + ',{"when": {"OR": [{"north": "none","east": "none","south": "none","west": "none"},{"north": "side|up","east": "side|up"},{"east": "side|up","south": "side|up"},{"south": "side|up","west": "side|up"},{"west": "side|up","north": "side|up"}]},"apply": {"model": "block/redstone_dust_dot"}},{"when": {"OR": [{"north": "side|up"},{"north": "none","east": "none","south": "side|up","west": "none"}]},"apply": {"model": "block/redstone_dust_side0"}},{"when": {"OR": [{"south": "side|up"},{"north": "side|up","east": "none","south": "none","west": "none"}]},"apply": {"model": "block/redstone_dust_side_alt0"}},{"when": {"OR": [{"east": "side|up"},{"north": "none","east": "none","south": "none","west": "side|up"}]},"apply": {"model": "block/redstone_dust_side_alt1","y": 270}},{"when": {"OR": [{"west": "side|up"},{"north": "none","east": "side|up","south": "none","west": "none"}]},"apply": {"model": "block/redstone_dust_side1","y": 270}},{"when": {"north": "up"},"apply": {"model": "block/redstone_dust_up"}},{"when": {"east": "up"},"apply": {"model": "block/redstone_dust_up","y": 90}},{"when": {"south": "up"},"apply": {"model": "block/redstone_dust_up","y": 180}},{"when": {"west": "up"},"apply": {"model": "block/redstone_dust_up","y": 270}}]}'
output = json.loads(output)

with open(r"resourcepack\assets\minecraft\blockstates\redstone_wire.json", "w") as f:
    json.dump(output, f, indent=4)


# --- models ---
for color in colors:
    print(f"Generating models for {color}")
    for power in range(16):
        model = {
            "textures": {
                f"{color}_{power}": f"block/{color}_{power}",
                "bg": "block/background"
            },

            "elements": [
                {
                    "from": [-16, -16, 32],
                    "to": [16, 32, 32],
                    "faces": {
                        "south": {
                            "uv": [0, 0, 16, 16],
                            "texture": f"#{color}_{power}",
                        }
                    }
                },
                {
                    "from": [-16, -16, 31.9],
                    "to": [16, 32, 31.9],
                    "faces": {
                        "south": {
                            "uv": [0,0,16,16],
                            "texture": "#bg"
                        }
                    }
                }
            ]
        }

        with open(f"resourcepack/assets/minecraft/models/block/{color}_{power}.json", "w") as f:
            json.dump(model, f, indent=4)


# --- textures ---
sample_texture = np.zeros((texture_size, texture_size, 3), dtype=np.uint8)

for y in range(sample_texture.shape[0]):
    for x in range(sample_texture.shape[1]):
        sample_texture[y, x, (y-x) % 3] = 17

default_texture = np.zeros((texture_size*3, texture_size*2, 3), dtype=np.uint8)
for y in range(3):
    for x in range(2):
        default_texture[y*texture_size:(y+1)*texture_size, x*texture_size:(x+1)*texture_size] = sample_texture

for color in range(len(colors)):
    print(f"Generating textures for {colors[color]}")
    for i in range(16):
        texture = np.zeros((texture_size*3, texture_size*2, 4), dtype=np.uint8)
        texture[:, :, color] = default_texture[:, :, color] * i
        texture[:, :, 3] = default_texture[:, :, color] * 15

        cv2.imwrite(f"resourcepack/assets/minecraft/textures/block/{colors[color]}_{i}.png", texture)
