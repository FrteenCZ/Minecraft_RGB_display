import cv2
import matplotlib.pyplot as plt
import numpy as np

input = cv2.imread("miku.png", cv2.IMREAD_COLOR)
input = cv2.resize(input, (100, 100))

output = np.zeros_like(input, dtype=np.uint8)

for y in range(-1, output.shape[0] + 1):
    for x in range(-1, output.shape[1]):
        if (y + x) % 2 == 0:

            y0 = np.clip(y - 1, 0, output.shape[0])
            y1 = np.clip(y + 2, 0, output.shape[0])
            x0 = np.clip(x, 0, output.shape[1])
            x1 = np.clip(x + 2, 0, output.shape[1])

            c = (y + 1) % 3
            output[y0:y1, x0:x1, c] = np.average(input[y0:y1, x0:x1, c])

cv2.imwrite("output.png", output)

plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
plt.show()
