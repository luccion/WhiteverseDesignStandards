# 制作天空颜色数据集
from PIL import Image
from datetime import timedelta

def export_pixels_to_file(image_path, output_path):
    # Open the image
    img = Image.open(image_path)

    # Get the RGB values of all pixels
    pixels = list(img.getdata())

    # Calculate the time increment for each pixel
    total_seconds = 24 * 60 * 60  # Total seconds in a day
    time_increment = total_seconds / len(pixels)

    # Open the output file
    with open(output_path, 'w') as file:
        # Write the RGB values to the file
        for i, pixel in enumerate(pixels):
            # Calculate the time for this pixel
            time = i * time_increment
                # Convert the time to HH:MM:SS format
            time_str = str(timedelta(seconds=int(time)))
            # Write the time and RGB values to the file
            file.write(f'{time_str},{pixel[0]},{pixel[1]},{pixel[2]}\n')


# Use the function
export_pixels_to_file('Preprocessing/skycolors48.png', 'Assets/Data/skycolors.csv')