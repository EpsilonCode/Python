from PIL import Image, ImageSequence
import os

def resize_image(file_path, new_height, output_folder):
    with Image.open(file_path) as img:
        # Calculate the new width maintaining the aspect ratio
        aspect_ratio = img.width / img.height
        new_width = int(aspect_ratio * new_height)

        # Resize the image or each frame in an animated image
        if getattr(img, "is_animated", False):
            frames = ImageSequence.Iterator(img)
            resized_frames = []

            for frame in frames:
                resized_frame = frame.copy()
                resized_frame = resized_frame.resize((new_width, new_height), Image.LANCZOS)
                resized_frames.append(resized_frame)

            # Save the animated image
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            output_file_path = os.path.join(output_folder, f"{file_name}.png")
            resized_frames[0].save(output_file_path, save_all=True, append_images=resized_frames[1:], loop=0)
        else:
            # Resize non-animated image
            resized_img = img.resize((new_width, new_height), Image.LANCZOS)
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            output_file_path = os.path.join(output_folder, f"{file_name}.png")
            resized_img.save(output_file_path)

            # Add watermark to the resized image
            add_watermark(output_file_path, watermark_path, position='lower_right', opacity=.55, watermark_size=(50, 45))  # Customize position, opacity, and watermark size

def add_watermark(input_image_path, watermark_image_path, position, opacity, watermark_size):
    base_image = Image.open(input_image_path)
    watermark = Image.open(watermark_image_path)

    # Resize the watermark image
    watermark = watermark.resize(watermark_size, Image.LANCZOS)

    # Adjust the opacity of the watermark
    watermark = watermark.convert("RGBA")
    watermark_with_opacity = Image.new("RGBA", watermark.size)
    for x in range(watermark.width):
        for y in range(watermark.height):
            r, g, b, a = watermark.getpixel((x, y))
            watermark_with_opacity.putpixel((x, y), (r, g, b, int(a * opacity)))

    # Paste the watermark onto the base image
    if base_image.mode != 'RGBA':
        base_image = base_image.convert('RGBA')
    watermark_layer = Image.new('RGBA', base_image.size, (0,0,0,0))
    if position == 'lower_right':
        position = (base_image.width - watermark_with_opacity.width, base_image.height - watermark_with_opacity.height)
    watermark_layer.paste(watermark_with_opacity, position, watermark_with_opacity)
    watermarked_image = Image.alpha_composite(base_image, watermark_layer)

    # Save the watermarked image
    watermarked_image.save(input_image_path)

# Replace these paths with your actual paths
folder_path = 'folder_path'
watermark_path = 'watermark_path/image.png'
output_folder = 'output_folder'


# Process images
for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.webp')):
        file_path = os.path.join(folder_path, filename)
        resize_image(file_path, 250, output_folder)


