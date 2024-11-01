
from PIL import Image
def add_border_if_needed(image_path, border_color=(255, 255, 255)):
    img = Image.open(image_path)
    width, height = img.size
    corners = [img.getpixel((0, 0)), img.getpixel((width-1, 0)), img.getpixel((0, height-1)), img.getpixel((width-1, height-1))]
    if all(corner == border_color for corner in corners):
        print("Image already has a border. No changes made.")
        return

    new_img = Image.new("RGB", (width+2, height+2), border_color)
    new_img.paste(img, (1, 1))
    new_image_path = "bordered_" + image_path
    new_img.save(new_image_path)
    print(f"Image saved with border as {new_image_path}")
image_path = "path/to/your/image.jpg"
add_border_if_needed(image_path)