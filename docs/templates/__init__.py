"""Collection of jinja2 templates to render md output."""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = Path(__file__).parent
file_loader = FileSystemLoader(str(TEMPLATE_DIR))
environment = Environment(loader=file_loader, autoescape=False)
get_template = environment.get_template

__all__ = [
    'get_template',
]
