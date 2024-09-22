import os
import cv2
import numpy as np

input_folder = 'croppedcellimages'
output_folder = 'croppedcellimages'

for folder in os.listdir(input_folder):
    folder_path = os.path.join(input_folder, folder)
    if os.path.isdir(folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                image_path = os.path.join(folder_path, filename)
                img = cv2.imread(image_path)

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                _, binary_image = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

                kernel = np.ones((2, 2), np.uint8)
                thickened = cv2.dilate(binary_image, kernel, iterations=1)
                final_image = cv2.bitwise_not(thickened)

                output_path = os.path.join(folder_path, filename)

                cv2.imwrite(output_path, final_image)

                print(f"Processed and saved: {output_path}")

print("Processing complete!")
