import pytest
import os
from PIL import Image, UnidentifiedImageError

# Adjust the Python path to import from the parent directory's image_tool module
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now we can import from image_tool.main
from image_tool import main as image_tool_main

# Define paths for test assets
BASE_DIR = os.path.dirname(__file__)
TEST_IMAGES_DIR = os.path.join(BASE_DIR, "test_images")
TEST_INPUT_IMAGE = os.path.join(TEST_IMAGES_DIR, "test_input.png") # Created in previous step (100x50 blue with red rect)
NOT_AN_IMAGE_FILE = os.path.join(TEST_IMAGES_DIR, "not_an_image.txt")

# Define a directory for temporary test outputs
TEST_OUTPUT_DIR = os.path.join(BASE_DIR, "test_outputs")
os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)

def clean_output_file(filepath):
    """Helper to remove a file if it exists."""
    if os.path.exists(filepath):
        os.remove(filepath)

# --- Tests for resize_image ---

def test_resize_success():
    output_path = os.path.join(TEST_OUTPUT_DIR, "resized_output.png")
    clean_output_file(output_path)
    target_width, target_height = 50, 25

    try:
        image_tool_main.resize_image(TEST_INPUT_IMAGE, output_path, target_width, target_height)
        assert os.path.exists(output_path), "Output image file was not created."
        with Image.open(output_path) as img:
            assert img.size == (target_width, target_height), f"Output image dimensions are {img.size}, expected ({target_width},{target_height})."
    finally:
        clean_output_file(output_path)

def test_resize_input_not_found(capsys):
    output_path = os.path.join(TEST_OUTPUT_DIR, "resize_fnf_output.png")
    clean_output_file(output_path)
    
    image_tool_main.resize_image("non_existent_input.png", output_path, 50, 50)
    captured = capsys.readouterr()
    assert "Error: Input file not found" in captured.out
    assert not os.path.exists(output_path), "Output file should not be created on input not found error."

def test_resize_input_not_image(capsys):
    output_path = os.path.join(TEST_OUTPUT_DIR, "resize_not_image_output.png")
    clean_output_file(output_path)

    image_tool_main.resize_image(NOT_AN_IMAGE_FILE, output_path, 50, 50)
    captured = capsys.readouterr()
    assert "Error: Cannot identify image file" in captured.out
    assert not os.path.exists(output_path), "Output file should not be created on invalid input image."

def test_resize_output_path_invalid(capsys):
    # Testing the scenario where the output directory doesn't exist
    invalid_output_path = os.path.join(TEST_OUTPUT_DIR, "non_existent_subdir", "output.png")
    # Ensure the sub-directory does not exist for this test
    if os.path.exists(os.path.dirname(invalid_output_path)):
        os.rmdir(os.path.dirname(invalid_output_path))

    image_tool_main.resize_image(TEST_INPUT_IMAGE, invalid_output_path, 50, 50)
    captured = capsys.readouterr()
    assert "Error saving image to" in captured.out # Expecting OSError message
    assert "No such file or directory" in captured.out # Specific OSError for non-existent dir
    assert not os.path.exists(invalid_output_path)


# --- Tests for create_thumbnail ---

def test_thumbnail_success():
    output_path = os.path.join(TEST_OUTPUT_DIR, "thumbnail_output.png")
    clean_output_file(output_path)
    target_size = 50 # Target max dimension (width or height)

    # Original image is 100x50. Thumbnail to 50x50 max size should result in 50x25.
    expected_width, expected_height = 50, 25 

    try:
        image_tool_main.create_thumbnail(TEST_INPUT_IMAGE, output_path, target_size)
        assert os.path.exists(output_path), "Thumbnail output file was not created."
        with Image.open(output_path) as img:
            assert img.size == (expected_width, expected_height), \
                f"Thumbnail dimensions are {img.size}, expected ({expected_width},{expected_height})."
            assert img.width <= target_size and img.height <= target_size, \
                f"Thumbnail dimensions {img.size} exceed target size {target_size}."
    finally:
        clean_output_file(output_path)

def test_thumbnail_input_not_found(capsys):
    output_path = os.path.join(TEST_OUTPUT_DIR, "thumb_fnf_output.png")
    clean_output_file(output_path)

    image_tool_main.create_thumbnail("non_existent_input.png", output_path, 50)
    captured = capsys.readouterr()
    assert "Error: Input file not found" in captured.out
    assert not os.path.exists(output_path)

def test_thumbnail_input_not_image(capsys):
    output_path = os.path.join(TEST_OUTPUT_DIR, "thumb_not_image_output.png")
    clean_output_file(output_path)

    image_tool_main.create_thumbnail(NOT_AN_IMAGE_FILE, output_path, 50)
    captured = capsys.readouterr()
    assert "Error: Cannot identify image file" in captured.out
    assert not os.path.exists(output_path)


# --- Tests for flip_image ---

def test_flip_horizontal_success():
    output_path = os.path.join(TEST_OUTPUT_DIR, "flipped_h_output.png")
    clean_output_file(output_path)
    try:
        image_tool_main.flip_image(TEST_INPUT_IMAGE, output_path, "horizontal")
        assert os.path.exists(output_path), "Horizontally flipped image file was not created."
        # Further validation could involve comparing pixels if a reference flipped image was available.
        # For now, checking size is a basic check.
        with Image.open(TEST_INPUT_IMAGE) as original_img:
            with Image.open(output_path) as flipped_img:
                assert original_img.size == flipped_img.size, "Flipped image dimensions differ from original."
    finally:
        clean_output_file(output_path)

def test_flip_vertical_success():
    output_path = os.path.join(TEST_OUTPUT_DIR, "flipped_v_output.png")
    clean_output_file(output_path)
    try:
        image_tool_main.flip_image(TEST_INPUT_IMAGE, output_path, "vertical")
        assert os.path.exists(output_path), "Vertically flipped image file was not created."
        with Image.open(TEST_INPUT_IMAGE) as original_img:
            with Image.open(output_path) as flipped_img:
                assert original_img.size == flipped_img.size, "Flipped image dimensions differ from original."
    finally:
        clean_output_file(output_path)

def test_flip_invalid_direction(capsys):
    output_path = os.path.join(TEST_OUTPUT_DIR, "flip_invalid_dir_output.png")
    clean_output_file(output_path)

    image_tool_main.flip_image(TEST_INPUT_IMAGE, output_path, "diagonal") # Invalid direction
    captured = capsys.readouterr()
    assert "Error: Invalid flip direction 'diagonal'" in captured.out
    assert not os.path.exists(output_path)

def test_flip_input_not_found(capsys):
    output_path = os.path.join(TEST_OUTPUT_DIR, "flip_fnf_output.png")
    clean_output_file(output_path)

    image_tool_main.flip_image("non_existent_input.png", output_path, "horizontal")
    captured = capsys.readouterr()
    assert "Error: Input file not found" in captured.out
    assert not os.path.exists(output_path)


# --- Tests for crop_image ---

def test_crop_success():
    output_path = os.path.join(TEST_OUTPUT_DIR, "cropped_output.png")
    clean_output_file(output_path)
    # Crop box: (left, top, right, bottom)
    # Original is 100x50. Crop to a 30x20 rectangle from (10,10).
    # So, left=10, top=10, right=10+30=40, bottom=10+20=30.
    crop_box = (10, 10, 40, 30) 
    expected_width, expected_height = 30, 20

    try:
        image_tool_main.crop_image(TEST_INPUT_IMAGE, output_path, *crop_box)
        assert os.path.exists(output_path), "Cropped image file was not created."
        with Image.open(output_path) as img:
            assert img.size == (expected_width, expected_height), \
                f"Cropped image dimensions are {img.size}, expected ({expected_width},{expected_height})."
    finally:
        clean_output_file(output_path)

def test_crop_input_not_found(capsys):
    output_path = os.path.join(TEST_OUTPUT_DIR, "crop_fnf_output.png")
    clean_output_file(output_path)
    crop_box = (0, 0, 10, 10)

    image_tool_main.crop_image("non_existent_input.png", output_path, *crop_box)
    captured = capsys.readouterr()
    assert "Error: Input file not found" in captured.out
    assert not os.path.exists(output_path)

# More crop tests could include:
# - Cropping outside image bounds (Pillow behavior is to adjust or return empty)
# - Crop box where right < left or bottom < top (Pillow might raise error or return empty)
# For now, these cover the main success and input error cases for the function itself.
# The CLI part in main() has checks for positive width/height of the crop *area*, not the coordinates.
