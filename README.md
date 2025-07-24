# Kiro Renderer

This is the official Python renderer for the Kiro markup language.

Kiro is a markup language designed for **meaningful writing**, maximizing **clarity of structure and style**.

This package provides both a library and a command-line interface (CLI) to convert `.kiro` files into HTML.

## Specification

The full specification for Kiro can be found in [docs/kiro_2.0.md](./docs/kiro_2.0.md).

## Installation

(This package is not yet available on PyPI.)

To install it locally for development:

```bash
pip install -e .
```

## Usage

### As a Library

```python
from kiro_renderer import render

kiro_text = """
# Hello Kiro

This is a paragraph.
"""

html_output = render(kiro_text)
print(html_output)
```

### As a Command-Line Tool

After installation, you can use the `kiro` command:

```bash
# Render a file and print to stdout
kiro examples/welcome.kiro

# Render a file and save to an output file
kiro examples/welcome.kiro -o output.html
```