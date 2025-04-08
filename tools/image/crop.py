from PIL import Image
import os
import argparse


def crop_image(
    input_path,
    output_path,
    crop_box=None,
    crop_center=False,
    crop_size=None,
    crop_percent=None,
):
    """
    Crop an image based on specified parameters.

    Args:
        input_path (str): Path to the input image
        output_path (str): Path where cropped image will be saved
        crop_box (tuple): Crop coordinates as (left, top, width, height)
        crop_center (bool): If True, crop from center using crop_size
        crop_size (tuple): Size for center crop (width, height)
        crop_percent (tuple): Percentage to crop from each edge (left, top, right, bottom)
    """
    with Image.open(input_path) as img:
        width, height = img.size

        # Determine crop box based on parameters
        if crop_box:
            # Convert (left, top, width, height) to (left, top, right, bottom)
            left, top, box_width, box_height = crop_box
            box = (left, top, left + box_width, top + box_height)
        elif crop_center and crop_size:
            # Crop from center
            center_x, center_y = width // 2, height // 2
            half_width, half_height = crop_size[0] // 2, crop_size[1] // 2
            box = (
                center_x - half_width,
                center_y - half_height,
                center_x + half_width,
                center_y + half_height,
            )
        elif crop_percent:
            # Calculate crop box based on percentages
            left_pct, top_pct, right_pct, bottom_pct = crop_percent
            box = (
                width * left_pct // 100,
                height * top_pct // 100,
                width * (100 - right_pct) // 100,
                height * (100 - bottom_pct) // 100,
            )
        else:
            # Default: no cropping, just copy the image
            box = (0, 0, width, height)

        # Ensure box is within image boundaries
        box = (max(0, box[0]), max(0, box[1]), min(width, box[2]), min(height, box[3]))

        # Crop the image
        cropped_img = img.crop(box)

        # Save the cropped image
        cropped_img.save(output_path)
        print(f"Image cropped to {cropped_img.size} and saved at {output_path}")


def process_directory(
    input_dir,
    output_dir,
    crop_box=None,
    crop_center=False,
    crop_size=None,
    crop_percent=None,
):
    """
    Crop all supported images in a directory.

    Args:
        input_dir (str): Directory containing input images
        output_dir (str): Directory where cropped images will be saved
        crop_box (tuple): Crop coordinates as (left, top, width, height)
        crop_center (bool): If True, crop from center using crop_size
        crop_size (tuple): Size for center crop (width, height)
        crop_percent (tuple): Percentage to crop from each edge (left, top, right, bottom)
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

            crop_image(
                input_path, output_path, crop_box, crop_center, crop_size, crop_percent
            )
            processed_count += 1

    print(f"Processed {processed_count} images from {input_dir}")


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Crop images using specified parameters"
    )
    parser.add_argument("input", help="Input image file or directory")
    parser.add_argument("output", help="Output image file or directory")

    # Cropping method group
    crop_group = parser.add_mutually_exclusive_group(required=True)
    crop_group.add_argument(
        "--box",
        type=int,
        nargs=4,
        metavar=("LEFT", "TOP", "WIDTH", "HEIGHT"),
        help="Crop box coordinates (left top width height)",
    )
    crop_group.add_argument(
        "--center", action="store_true", help="Crop from the center of the image"
    )
    crop_group.add_argument(
        "--percent",
        type=int,
        nargs=4,
        metavar=("LEFT", "TOP", "RIGHT", "BOTTOM"),
        help="Crop percentages from each edge (0-100)",
    )

    # Center crop size
    parser.add_argument(
        "--size",
        type=int,
        nargs=2,
        metavar=("WIDTH", "HEIGHT"),
        help="Width and height for center crop (required with --center)",
    )

    # Parse arguments
    args = parser.parse_args()

    # Handle cropping method
    crop_box = None
    crop_center = False
    crop_size = None
    crop_percent = None

    if args.box:
        # Direct box coordinates (left, top, width, height)
        crop_box = tuple(args.box)
    elif args.center:
        # Center cropping
        if not args.size:
            parser.error("--center requires --size")
        crop_center = True
        crop_size = tuple(args.size)
    elif args.percent:
        # Percentage cropping
        crop_percent = tuple(args.percent)

    # Check if input is a file or directory
    if os.path.isfile(args.input):
        # Single file processing
        crop_image(
            args.input, args.output, crop_box, crop_center, crop_size, crop_percent
        )
    elif os.path.isdir(args.input):
        # Directory processing
        process_directory(
            args.input, args.output, crop_box, crop_center, crop_size, crop_percent
        )
    else:
        print(f"Error: Input path '{args.input}' does not exist")
        return 1

    return 0


if __name__ == "__main__":
    main()
