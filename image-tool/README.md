# Image Manipulation CLI

This project is a Python-based CLI utility for performing common image manipulation tasks. It's designed to demonstrate effective project organization and modern Python development practices.

## Purpose

- Create a functional Python CLI tool for image manipulation
- Demonstrate best practices in Python project structure
- Showcase modern development workflows with Poetry and testing

## Technology Stack

- **Python**: Core programming language
- **Pillow**: Industry-standard Python Imaging Library
- **Poetry**: Dependency management and packaging
- **Ruff**: Modern Python linter and formatter
- **pytest**: Testing framework

## Features

The CLI tool provides the following image manipulation capabilities:

- Cropping images to specified dimensions
- Scaling images while maintaining aspect ratio
- Flipping images (horizontal/vertical)
- Generating thumbnails with custom sizes

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/jordanblakey/jules-experiments.git
   cd jules-experiments/image-tool
   ```

2. **Install Poetry:**

   ```bash
   pip install poetry
   ```

   For alternative installation methods, visit the [Poetry documentation](https://python-poetry.org/docs/#installation).

3. **Install dependencies:**
   ```bash
   poetry install
   ```

## Usage

Run commands using poetry run:

```bash
poetry run python -m image_tool --help
```

Common commands:

```bash
# Resize an image
poetry run python -m image_tool resize input.jpg --width 800 --height 600

# Create a thumbnail
poetry run python -m image_tool thumbnail input.jpg --size 200

# Flip an image horizontally
poetry run python -m image_tool flip input.jpg --direction horizontal
```

## Development

1. **Run tests:**

   ```bash
   poetry run pytest
   ```

2. **Check code style:**

   ```bash
   poetry run ruff check .
   ```

3. **Format code:**

   ```bash
   poetry run ruff format .
   ```

4. **Build package:**
   ```bash
   poetry build
   ```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
