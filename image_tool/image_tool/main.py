import argparse
from PIL import Image, UnidentifiedImageError

def resize_image(input_path, output_path, width, height):
    """Resizes an image to the specified width and height."""
    try:
        img = Image.open(input_path)
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
        return
    except UnidentifiedImageError:
        print(f"Error: Cannot identify image file. The file at {input_path} may be corrupted or not a valid image.")
        return
    except Exception as e: # Catch any other error during open
        print(f"An error occurred while opening image {input_path}: {e}")
        return

    try:
        resized_img = img.resize((width, height))
        resized_img.save(output_path)
        print(f"Image resized successfully and saved to {output_path}")
    except OSError as e:
        print(f"Error saving image to {output_path}: {e}")
    except Exception as e:
        print(f"An error occurred during image processing or saving: {e}")

def create_thumbnail(input_path, output_path, size=128):
    """Creates a thumbnail of an image."""
    try:
        img = Image.open(input_path)
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
        return
    except UnidentifiedImageError:
        print(f"Error: Cannot identify image file. The file at {input_path} may be corrupted or not a valid image.")
        return
    except Exception as e: # Catch any other error during open
        print(f"An error occurred while opening image {input_path}: {e}")
        return

    try:
        img.thumbnail((size, size))
        img.save(output_path)
        print(f"Thumbnail created successfully and saved to {output_path}")
    except OSError as e:
        print(f"Error saving image to {output_path}: {e}")
    except Exception as e:
        print(f"An error occurred during image processing or saving: {e}")

def flip_image(input_path, output_path, direction):
    """Flips an image horizontally or vertically."""
    try:
        img = Image.open(input_path)
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
        return
    except UnidentifiedImageError:
        print(f"Error: Cannot identify image file. The file at {input_path} may be corrupted or not a valid image.")
        return
    except Exception as e: # Catch any other error during open
        print(f"An error occurred while opening image {input_path}: {e}")
        return

    try:
        if direction == "horizontal":
            flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)
        elif direction == "vertical":
            flipped_img = img.transpose(Image.FLIP_TOP_BOTTOM)
        else:
            # This case should ideally be prevented by argparse choices,
            # but as a safeguard for direct function calls:
            print(f"Error: Invalid flip direction '{direction}'. Choose 'horizontal' or 'vertical'.")
            return
        flipped_img.save(output_path)
        print(f"Image flipped {direction}ly and saved to {output_path}")
    except OSError as e:
        print(f"Error saving image to {output_path}: {e}")
    except Exception as e:
        print(f"An error occurred during image processing or saving: {e}")

def crop_image(input_path, output_path, left, top, right, bottom):
    """Crops an image to the specified coordinates (left, top, right, bottom)."""
    try:
        img = Image.open(input_path)
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
        return
    except UnidentifiedImageError:
        print(f"Error: Cannot identify image file. The file at {input_path} may be corrupted or not a valid image.")
        return
    except Exception as e: # Catch any other error during open
        print(f"An error occurred while opening image {input_path}: {e}")
        return

    try:
        cropped_img = img.crop((left, top, right, bottom))
        cropped_img.save(output_path)
        print(f"Image cropped successfully and saved to {output_path}")
    except OSError as e:
        print(f"Error saving image to {output_path}: {e}")
    except Exception as e:
        print(f"An error occurred during image processing or saving: {e}")

def main():
    parser = argparse.ArgumentParser(description="A simple image manipulation tool.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Resize command
    resize_parser = subparsers.add_parser("resize", help="Resize an image")
    resize_parser.add_argument("input_file", help="Path to the input image file")
    resize_parser.add_argument("output_file", help="Path to save the resized image")
    resize_parser.add_argument("--width", type=int, help="New width for the image")
    resize_parser.add_argument("--height", type=int, help="New height for the image")

    # Thumbnail command
    thumbnail_parser = subparsers.add_parser("thumbnail", help="Create a thumbnail for an image")
    thumbnail_parser.add_argument("input_file", help="Path to the input image file")
    thumbnail_parser.add_argument("output_file", help="Path to save the thumbnail")
    thumbnail_parser.add_argument("--size", type=int, default=128, help="Size of the thumbnail (default: 128x128)")

    # Flip command
    flip_parser = subparsers.add_parser("flip", help="Flip an image")
    flip_parser.add_argument("input_file", help="Path to the input image file")
    flip_parser.add_argument("output_file", help="Path to save the flipped image")
    flip_parser.add_argument("--direction", choices=["horizontal", "vertical"], required=True, help="Direction to flip (horizontal or vertical)")

    # Crop command
    crop_parser = subparsers.add_parser("crop", help="Crop an image")
    crop_parser.add_argument("input_file", help="Path to the input image file")
    crop_parser.add_argument("output_file", help="Path to save the cropped image")
    crop_parser.add_argument("--x", type=int, required=True, help="X-coordinate of the top-left corner of the crop area")
    crop_parser.add_argument("--y", type=int, required=True, help="Y-coordinate of the top-left corner of the crop area")
    crop_parser.add_argument("--width", type=int, required=True, help="Width of the crop area")
    crop_parser.add_argument("--height", type=int, required=True, help="Height of the crop area")

    args = parser.parse_args()

    if args.command:
        if args.command == "resize":
            if args.width is None or args.height is None:
                # This check is important because argparse doesn't enforce that both are present,
                # only that if --width or --height is given, it's an int.
                # The resize_parser could be modified to make them conditionally required or group them.
                # For now, explicit check after parsing.
                print("Error: Both --width and --height are required for resize.")
                # resize_parser.print_help() # Optionally print help for the specific command
            else:
                resize_image(args.input_file, args.output_file, args.width, args.height)
        elif args.command == "thumbnail":
            create_thumbnail(args.input_file, args.output_file, args.size)
        elif args.command == "flip":
            flip_image(args.input_file, args.output_file, args.direction)
        elif args.command == "crop":
            # Convert x, y, width, height to left, top, right, bottom
            # as expected by the crop_image function and Pillow's crop.
            left = args.x
            top = args.y
            right = args.x + args.width
            bottom = args.y + args.height
            if args.width <= 0 or args.height <= 0:
                print("Error: Crop width and height must be positive values.")
            else:
                crop_image(args.input_file, args.output_file, left, top, right, bottom)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
