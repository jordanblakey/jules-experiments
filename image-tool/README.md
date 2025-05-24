# Image Manipulation CLI

This project is a Python-based CLI utility for performing common image manipulation tasks. It's also an experiment in learning to work with Jules, exploring project configuration, and collaborating on software development.

## Purpose

*   Learn about working with the AI coding assistant, Jules.
*   Explore workflows for providing direction, reviewing PRs, and basic project configuration.
*   Create a functional Python CLI tool for image manipulation.

## Technology Choices

*   **Python**: The core language for the CLI tool.
*   **Pillow**: A Python Imaging Library for image manipulation functionalities.
*   **Ruff**: For code formatting and linting to maintain code quality.

## Planned Functionality

The CLI tool aims to provide the following image manipulation features:
*   Cropping
*   Scaling
*   Flipping (horizontal/vertical)
*   Generating thumbnails

## Getting Started

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name> 
    ```
    *(Replace `<repository-url>` and `<repository-name>` with the actual URL and name)*

2.  **Install Poetry:**
    If you don't have Poetry installed, please follow the instructions on the [official Poetry website](https://python-poetry.org/docs/#installation).

3.  **Install dependencies:**
    Navigate to the project root (where `pyproject.toml` is located) and run:
    ```bash
    poetry install
    ```
    This will create a virtual environment if one doesn't exist and install all necessary dependencies.

4.  **Run the tool:**
    To run the CLI tool, use:
    ```bash
    poetry run python image_tool.py --help
    ```
    *(Note: The CLI tool is currently under development. The entry point `image_tool.py` is a placeholder.)*

5.  **Running Tests (Placeholder):**
    Once tests are added, you'll be able to run them using a command like:
    ```bash
    poetry run pytest 
    ```

6.  **Building the project (Placeholder):**
    To build the project (e.g., for distribution), you can use:
    ```bash
    poetry build
    ```

## How to Contribute

Details on how to contribute will be added soon. We encourage collaboration and feedback!
