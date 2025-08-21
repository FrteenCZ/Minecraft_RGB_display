import cv2
import matplotlib.pyplot as plt
import numpy as np

# Load an image (color)
image = cv2.imread("miku.png", cv2.IMREAD_COLOR)

image = cv2.resize(image, (100, 100))

img = np.zeros((image.shape[0] + 2, image.shape[1], image.shape[2]), dtype=np.float32)
img[2:, :, :] = image

for i in range(2):
    img[i, :, :] = img[2, :, :]



kernel_x_size = 2
kernel_y_size = 3

# Create an output image
print(f"Image shape: {img.shape}")
output = np.zeros_like(img, dtype=np.float32)
print(f"Image shape: {output.shape}")

# Loop over blocks without overlap
for channel in range(output.shape[2]):  
    for y in range(0, output.shape[0], kernel_y_size):
        y += channel
        for x in range(0, output.shape[1], kernel_x_size):
            block = img[y:y+kernel_y_size, x:x+kernel_x_size]
        
            # Compute mean of the block
            mean_val = np.mean(block[:, :, channel], dtype=np.float32)
            
            # Fill the block in the output with that mean
            output[y:y+kernel_y_size, x:x+kernel_x_size, channel] = mean_val

output = output[2:, :, :]

cv2.imwrite("output.png", output)

plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB)// 16 * 16 / 255.0)
plt.show()

if __name__ == "__main__":
    pass
