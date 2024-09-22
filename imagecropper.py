import os
from PIL import Image

input_folder = 'cellimages'
output_folder = 'croppedcellimages'

crop_size = (98, 98)

def crop_center(image, crop_width, crop_height):
    width, height = image.size
    left = (width - crop_width) / 2
    top = (height - crop_height) / 2
    right = (width + crop_width) / 2
    bottom = (height + crop_height) / 2
    return image.crop((left, top, right, bottom))

for filename in os.listdir(input_folder):
    if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        image_path = os.path.join(input_folder, filename)
        with Image.open(image_path) as img:
            cropped_img = crop_center(img, *crop_size)
            output_path = os.path.join(output_folder, filename)
            cropped_img.save(output_path)
            print(f"Cropped and saved: {output_path}")

print("Processing complete!")