import os
import shutil

import pytest
from PIL import Image

# Ensure src.main can be imported.
# This assumes that pytest is run from the 'image-tool' directory,
# or that PYTHONPATH is set up so that 'src' is discoverable.
# An alternative is to adjust sys.path here, but it's cleaner if the test runner handles it.
from src import main as image_tool_main

# --- Pytest Fixture for Test Environment ---


@pytest.fixture(
    scope="module"
)  # Use "module" scope for efficiency if test image creation is slow
def test_env():
    base_dir = os.path.dirname(__file__)
    test_images_dir = os.path.join(base_dir, "test_images_temp")
    test_outputs_dir = os.path.join(base_dir, "test_outputs_temp")

    # Create directories
    os.makedirs(test_images_dir, exist_ok=True)
    os.makedirs(test_outputs_dir, exist_ok=True)

    # Create a dummy input image
    test_input_image_path = os.path.join(test_images_dir, "test_input.png")
    try:
        img = Image.new("RGB", (10, 10), color="red")
        img.save(test_input_image_path)
    except Exception as e:
        pytest.fail(f"Failed to create test input image: {e}")

    # Create a non-image file
    not_an_image_path = os.path.join(test_images_dir, "not_an_image.txt")
    try:
        with open(not_an_image_path, "w") as f:
            f.write("This is not an image file.")
    except Exception as e:
        pytest.fail(f"Failed to create not_an_image.txt: {e}")

    env_paths = {
        "input_image": test_input_image_path,
        "not_an_image": not_an_image_path,
        "outputs_dir": test_outputs_dir,
    }

    yield env_paths  # Provide paths to the tests

    # Teardown: Remove temporary directories
    try:
        shutil.rmtree(test_images_dir)
        shutil.rmtree(test_outputs_dir)
    except Exception as e:
        print(f"Error during test cleanup: {e}")


def get_output_path(test_env_fixture, filename):
    """Helper to get a unique output path for a test."""
    return os.path.join(test_env_fixture["outputs_dir"], filename)


# --- Tests for resize_image ---


def test_resize_success(test_env, capsys):
    output_path = get_output_path(test_env, "resized.png")
    target_w, target_h = 5, 5
    image_tool_main.resize_image(
        test_env["input_image"], output_path, target_w, target_h
    )
    assert os.path.exists(output_path)
    with Image.open(output_path) as img:
        assert img.size == (target_w, target_h)
    captured = capsys.readouterr()
    assert (
        f"Image resized successfully and saved to {output_path}" in captured.out
    )


def test_resize_input_not_found(test_env, capsys):
    output_path = get_output_path(test_env, "resize_fnf.png")
    image_tool_main.resize_image("non_existent.png", output_path, 5, 5)
    captured = capsys.readouterr()
    assert "Error: Input file not found" in captured.out
    assert not os.path.exists(output_path)


def test_resize_input_not_image(test_env, capsys):
    output_path = get_output_path(test_env, "resize_not_img.png")
    image_tool_main.resize_image(test_env["not_an_image"], output_path, 5, 5)
    captured = capsys.readouterr()
    assert "Error: Cannot identify image file" in captured.out
    assert not os.path.exists(output_path)


def test_resize_output_invalid_path(test_env, capsys):
    invalid_out_path = os.path.join(
        test_env["outputs_dir"], "invalid_dir/resized.png"
    )
    image_tool_main.resize_image(
        test_env["input_image"], invalid_out_path, 5, 5
    )
    captured = capsys.readouterr()
    assert "Error saving image to" in captured.out
    assert not os.path.exists(invalid_out_path)


# --- Tests for create_thumbnail ---


def test_thumbnail_success(test_env, capsys):
    output_path = get_output_path(test_env, "thumb.png")
    # Original 10x10, thumb size 5. Expected output 5x5.
    target_size, expected_w, expected_h = 5, 5, 5
    image_tool_main.create_thumbnail(
        test_env["input_image"], output_path, target_size
    )
    assert os.path.exists(output_path)
    with Image.open(output_path) as img:
        assert img.size == (expected_w, expected_h)
    captured = capsys.readouterr()
    assert (
        f"Thumbnail created successfully and saved to {output_path}"
        in captured.out
    )


def test_thumbnail_input_not_found(test_env, capsys):
    output_path = get_output_path(test_env, "thumb_fnf.png")
    image_tool_main.create_thumbnail("non_existent.png", output_path, 5)
    captured = capsys.readouterr()
    assert "Error: Input file not found" in captured.out
    assert not os.path.exists(output_path)


def test_thumbnail_input_not_image(test_env, capsys):
    output_path = get_output_path(test_env, "thumb_not_img.png")
    image_tool_main.create_thumbnail(test_env["not_an_image"], output_path, 5)
    captured = capsys.readouterr()
    assert "Error: Cannot identify image file" in captured.out
    assert not os.path.exists(output_path)


def test_thumbnail_output_invalid_path(test_env, capsys):
    invalid_out_path = os.path.join(
        test_env["outputs_dir"], "invalid_dir/thumb.png"
    )
    image_tool_main.create_thumbnail(
        test_env["input_image"], invalid_out_path, 5
    )
    captured = capsys.readouterr()
    assert "Error saving image to" in captured.out
    assert not os.path.exists(invalid_out_path)


# --- Tests for flip_image ---


def test_flip_horizontal_success(test_env, capsys):
    output_path = get_output_path(test_env, "flipped_h.png")
    image_tool_main.flip_image(
        test_env["input_image"], output_path, "horizontal"
    )
    assert os.path.exists(output_path)
    captured = capsys.readouterr()
    assert (
        f"Image flipped horizontally and saved to {output_path}" in captured.out
    )


def test_flip_vertical_success(test_env, capsys):
    output_path = get_output_path(test_env, "flipped_v.png")
    image_tool_main.flip_image(test_env["input_image"], output_path, "vertical")
    assert os.path.exists(output_path)
    captured = capsys.readouterr()
    assert (
        f"Image flipped vertically and saved to {output_path}" in captured.out
    )


def test_flip_input_not_found(test_env, capsys):
    output_path = get_output_path(test_env, "flip_fnf.png")
    image_tool_main.flip_image("non_existent.png", output_path, "horizontal")
    captured = capsys.readouterr()
    assert "Error: Input file not found" in captured.out
    assert not os.path.exists(output_path)


def test_flip_input_not_image(
    test_env, capsys
):  # Added this test for completeness
    output_path = get_output_path(test_env, "flip_not_img.png")
    image_tool_main.flip_image(
        test_env["not_an_image"], output_path, "horizontal"
    )
    captured = capsys.readouterr()
    assert "Error: Cannot identify image file" in captured.out
    assert not os.path.exists(output_path)


def test_flip_output_invalid_path(test_env, capsys):
    invalid_out_path = os.path.join(
        test_env["outputs_dir"], "invalid_dir/flipped.png"
    )
    image_tool_main.flip_image(
        test_env["input_image"], invalid_out_path, "horizontal"
    )
    captured = capsys.readouterr()
    assert "Error saving image to" in captured.out
    assert not os.path.exists(invalid_out_path)


# --- Tests for crop_image ---


def test_crop_success(test_env, capsys):
    output_path = get_output_path(test_env, "cropped.png")
    # Original 10x10. Crop: left=2, top=2, right=8, bottom=8. Expected 6x6.
    crop_box = (2, 2, 8, 8)
    expected_w, expected_h = 6, 6
    image_tool_main.crop_image(test_env["input_image"], output_path, *crop_box)
    assert os.path.exists(output_path)
    with Image.open(output_path) as img:
        assert img.size == (expected_w, expected_h)
    captured = capsys.readouterr()
    assert (
        f"Image cropped successfully and saved to {output_path}" in captured.out
    )


def test_crop_input_not_found(test_env, capsys):
    output_path = get_output_path(test_env, "crop_fnf.png")
    image_tool_main.crop_image("non_existent.png", output_path, 0, 0, 5, 5)
    captured = capsys.readouterr()
    assert "Error: Input file not found" in captured.out
    assert not os.path.exists(output_path)


def test_crop_input_not_image(
    test_env, capsys
):  # Added this test for completeness
    output_path = get_output_path(test_env, "crop_not_img.png")
    image_tool_main.crop_image(
        test_env["not_an_image"], output_path, 0, 0, 5, 5
    )
    captured = capsys.readouterr()
    assert "Error: Cannot identify image file" in captured.out
    assert not os.path.exists(output_path)


def test_crop_output_invalid_path(test_env, capsys):
    invalid_out_path = os.path.join(
        test_env["outputs_dir"], "invalid_dir/cropped.png"
    )
    image_tool_main.crop_image(
        test_env["input_image"], invalid_out_path, 0, 0, 5, 5
    )
    captured = capsys.readouterr()
    assert "Error saving image to" in captured.out
    assert not os.path.exists(invalid_out_path)
