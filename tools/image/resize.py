from PIL import Image
import os
import argparse


def resize_image(input_path, output_path, size=(120, 120)):
    """
    Resize an image to the specified size.

    Args:
        input_path (str): Path to the input image
        output_path (str): Path where resized image will be saved
        size (tuple): Target size (width, height)
    """
    # Open the image
    with Image.open(input_path) as img:
        # Resize the image
        resized_img = img.resize(size, Image.Resampling.LANCZOS)

        # Save the resized image
        resized_img.save(output_path)
        print(f"Image resized to {size} and saved at {output_path}")


def process_directory(input_dir, output_dir, size=(120, 120)):
    """
    Resize all supported images in a directory.

    Args:
        input_dir (str): Directory containing input images
        output_dir (str): Directory where resized images will be saved
        size (tuple): Target size (width, height)
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Supported image formats
    supported_formats = (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".gif")
    processed_count = 0

    # Process each file in the input directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(supported_formats):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            resize_image(input_path, output_path, size)
            processed_count += 1

    print(f"Processed {processed_count} images from {input_dir}")


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Resize images to specified dimensions"
    )
    parser.add_argument("input", help="Input image file or directory")
    parser.add_argument("output", help="Output image file or directory")
    parser.add_argument(
        "--width", type=int, default=120, help="Output width (default: 120)"
    )
    parser.add_argument(
        "--height", type=int, default=120, help="Output height (default: 120)"
    )

    # Parse arguments
    args = parser.parse_args()
    size = (args.width, args.height)

    # Check if input is a file or directory
    if os.path.isfile(args.input):
        # Single file processing
        resize_image(args.input, args.output, size)
    elif os.path.isdir(args.input):
        # Directory processing
        process_directory(args.input, args.output, size)
    else:
        print(f"Error: Input path '{args.input}' does not exist")
        return 1

    return 0


if __name__ == "__main__":
    main()
