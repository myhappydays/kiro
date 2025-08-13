from .parser import KiroParser
from .renderer import KiroRenderer

def render(text: str) -> str:
    """The main entry point for rendering Kiro text to HTML."""
    parser = KiroParser(text)
    ast = parser.parse()
    
    renderer = KiroRenderer()
    html_output = renderer.render(ast)
    
    return html_output
