from PIL import Image
import os
import argparse
import numpy as np


def transparency_to_green(
    input_path, output_path, green_color=(0, 255, 0), alpha_threshold=128
):
    """
    Convert transparent areas of an image to green.

    Args:
        input_path (str): Path to the input image
        output_path (str): Path where the green-backed image will be saved
        green_color (tuple): RGB color to use for transparent areas (default: pure green)
        alpha_threshold (int): Alpha values below this will be replaced with green (0-255)
    """
    # Open the image with transparency
    with Image.open(input_path) as img:
        # Make sure we handle images with and without alpha channel
        if img.mode == "RGBA":
            # Image already has alpha channel
            pass
        elif img.mode == "RGB":
            # No alpha channel - nothing to replace
            print(f"Warning: Image {input_path} has no transparency, saving as is")
            img.save(output_path)
            return
        else:
            # Convert other formats to RGBA
            img = img.convert("RGBA")

        # Convert to numpy array for faster processing
        img_array = np.array(img)

        # Create a mask of transparent pixels
        # Alpha channel is the 4th channel (index 3)
        transparent_mask = img_array[:, :, 3] < alpha_threshold

        # Create a copy of the image
        result = img_array.copy()

        # Replace transparent pixels with green
        result[transparent_mask, 0] = green_color[0]  # R
        result[transparent_mask, 1] = green_color[1]  # G
        result[transparent_mask, 2] = green_color[2]  # B
        result[transparent_mask, 3] = 255  # A (fully opaque)

        # Convert back to PIL Image and save
        result_img = Image.fromarray(result)

        # Convert to RGB mode if output format doesn't support alpha
        output_ext = os.path.splitext(output_path)[1].lower()
        if output_ext in [".jpg", ".jpeg", ".bmp"]:
            result_img = result_img.convert("RGB")

        result_img.save(output_path)
        print(f"Converted transparent areas to green in {output_path}")


def process_directory(
    input_dir, output_dir, green_color=(0, 255, 0), alpha_threshold=128
):
    """
    Process all supported images in a directory.

    Args:
        input_dir (str): Directory containing input images
        output_dir (str): Directory where processed images will be saved
        green_color (tuple): RGB color to use for transparent areas
        alpha_threshold (int): Alpha values below this will be replaced
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Supported image formats
    supported_formats = (
        ".png",
        ".tga",
        ".tiff",
        ".webp",
    )  # Formats that support transparency
    processed_count = 0

    # Process each file in the input directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(supported_formats):
            input_path = os.path.join(input_dir, filename)

            # Determine output filename
            name, ext = os.path.splitext(filename)
            output_filename = filename

            # If saving to formats that don't support transparency, convert to PNG
            if args.force_png:
                output_filename = f"{name}.png"

            output_path = os.path.join(output_dir, output_filename)

            transparency_to_green(input_path, output_path, green_color, alpha_threshold)
            processed_count += 1

    print(f"Processed {processed_count} images from {input_dir}")


def parse_color(color_str):
    """Parse color string in format 'R,G,B'"""
    try:
        r, g, b = map(int, color_str.split(","))
        if not all(0 <= c <= 255 for c in (r, g, b)):
            raise ValueError("Color values must be between 0 and 255")
        return (r, g, b)
    except Exception as e:
        raise argparse.ArgumentTypeError(f"Invalid color format: {e}")


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Convert transparent areas of images to green"
    )
    parser.add_argument("input", help="Input image file or directory")
    parser.add_argument("output", help="Output image file or directory")
    parser.add_argument(
        "--color",
        type=parse_color,
        default="0,255,0",
        help="RGB color to use for transparent areas (format: R,G,B)",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=128,
        help="Alpha threshold (0-255, default: 128)",
    )
    parser.add_argument(
        "--force-png",
        action="store_true",
        help="Force output to PNG format to preserve quality",
    )

    # Parse arguments
    global args
    args = parser.parse_args()

    green_color = args.color
    alpha_threshold = max(0, min(255, args.threshold))  # Ensure value is between 0-255

    # Check if input is a file or directory
    if os.path.isfile(args.input):
        # Single file processing
        transparency_to_green(args.input, args.output, green_color, alpha_threshold)
    elif os.path.isdir(args.input):
        # Directory processing
        process_directory(args.input, args.output, green_color, alpha_threshold)
    else:
        print(f"Error: Input path '{args.input}' does not exist")
        return 1

    return 0


if __name__ == "__main__":
    main()
