from PIL import Image, ImageOps
import os

# Input and output directories
input_folder = "input_images"  # Folder containing original images
output_folder = "output_images"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Target size
TARGET_SIZE = (300, 300)

# Process all images in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path).convert("RGBA")  # Ensure image has an alpha channel

        # Resize while keeping aspect ratio
        img.thumbnail(TARGET_SIZE, Image.LANCZOS)  # Resizes to fit within 300x300

        # Create transparent background
        transparent_bg = Image.new("RGBA", TARGET_SIZE, (255, 255, 255, 255))

        # Paste resized image onto transparent background (centered)
        x_offset = (TARGET_SIZE[0] - img.width) // 2
        y_offset = (TARGET_SIZE[1] - img.height) // 2
        transparent_bg.paste(img, (x_offset, y_offset), img)

        # Save output image (ensure PNG to keep transparency)
        output_path = os.path.join(output_folder, filename.split('.')[0] + ".png")
        transparent_bg.save(output_path, format="PNG")

print(f"Processed images saved in '{output_folder}'")
