import streamlit as st
from PIL import Image, ImageOps
import io

st.title("Image Resizer with Background Fill")

# File uploader for multiple images
uploaded_files = st.file_uploader("Upload one or more images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Inputs for width and height
width = st.number_input("Enter width", min_value=1, value=512)
height = st.number_input("Enter height", min_value=1, value=512)

# Color picker
bg_color = st.color_picker("Pick a background color", "#FFFFFF")
alpha = st.slider("Opacity (0-255)", 0, 255, 255)

# Process images
if uploaded_files:
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        image = image.convert("RGBA")  # Ensure proper transparency handling
        
        # Create a new image with the desired size and background color
        rgba_color = (*ImageColor.getrgb(bg_color), alpha)
        new_image = Image.new("RGBA", (width, height), rgba_color)
        image.thumbnail((width, height), Image.LANCZOS)
        
        # Center the image on the new canvas
        x_offset = (width - image.width) // 2
        y_offset = (height - image.height) // 2
        new_image.paste(image, (x_offset, y_offset), image)
        
        # Convert to RGB if needed (to remove alpha channel)
        new_image = new_image.convert("RGB")
        
        # Prepare image for download
        img_byte_arr = io.BytesIO()
        new_image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        st.image(new_image, caption=f"Processed {uploaded_file.name}", use_container_width=True)
        st.download_button(label=f"Download {uploaded_file.name}", data=img_byte_arr, file_name=f"processed_{uploaded_file.name}", mime="image/png")
