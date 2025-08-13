from dataclasses import dataclass, field
from typing import List, Any, Optional, Dict

# --- Base Nodes ---

@dataclass
class Node:
    """The base class for all AST nodes."""
    pass

@dataclass
class StyleDefinition(Node):
    """Represents a parsed style definition from a <style> block."""
    name: str
    properties: Dict[str, str] = field(default_factory=dict) # e.g., {"color": "#444", "tailwind": "text-lg"}
    is_global: bool = False

@dataclass
class DocumentNode(Node):
    """The root node of the document's AST."""
    children: List[Node] = field(default_factory=list)
    styles: Dict[str, StyleDefinition] = field(default_factory=dict) # For storing parsed StyleDefinition objects
    footnotes: dict = field(default_factory=dict) # For storing footnote definitions

# --- Block Nodes ---

@dataclass
class ParagraphNode(Node):
    """Represents a paragraph of text."""
    children: List[Node] = field(default_factory=list)

@dataclass
class HeadingNode(Node):
    """Represents a heading (e.g., # My Title)."""
    level: int
    children: List[Node] = field(default_factory=list)

@dataclass
class HorizontalRuleNode(Node):
    """Represents a horizontal rule (---)."""
    pass

@dataclass
class CodeBlockNode(Node):
    """Represents a code block (```...```)."""
    language: Optional[str] = None
    content: str = ""

@dataclass
class QuoteNode(Node):
    """Represents a blockquote (| ...)."""
    children: List[Node] = field(default_factory=list)

@dataclass
class ListItemNode(Node):
    """Represents a standard list item (- or *)."""
    children: List[Node] = field(default_factory=list)
    level: int = 0 # For nested lists

@dataclass
class OrderedListItemNode(Node):
    """Represents a report-style ordered list item (-1.A.)."""
    prefix: str # e.g., "1.", "A."
    children: List[Node] = field(default_factory=list)
    level: int = 0 # For nested lists

@dataclass
class ToggleNode(Node):
    """Represents a toggle block (> ...)."""
    summary: List[Node] = field(default_factory=list)
    content: List[Node] = field(default_factory=list)

@dataclass
class StyleBlockNode(Node):
    """Represents a <style> block. Its content is processed by the parser, not rendered directly."""
    content: str = ""

@dataclass
class FootnoteDefinitionNode(Node):
    """Represents a footnote definition ([^id]: ...)."""
    id: str
    children: List[Node] = field(default_factory=list)

@dataclass
class MacroNode(Node):
    """Represents a macro (e.g., !youtube(...))."""
    name: str
    args: List[str] = field(default_factory=list)

# --- Inline Nodes ---

@dataclass
class TextNode(Node):
    """Represents plain text content."""
    text: str

@dataclass
class BoldNode(Node):
    """Represents bold text (**...**)."""
    children: List[Node] = field(default_factory=list)

@dataclass
class EmphasisNode(Node):
    """Represents emphasized (italic) text (*...*)."""
    children: List[Node] = field(default_factory=list)

@dataclass
class StrikethroughNode(Node):
    """Represents strikethrough text (~~...~~)."""
    children: List[Node] = field(default_factory=list)

@dataclass
class InlineCodeNode(Node):
    """Represents inline code (`...`)."""
    text: str

@dataclass
class FootnoteRefNode(Node):
    """Represents a footnote reference ([^id])."""
    id: str

@dataclass
class StyleSpanNode(Node):
    """Represents a style span ([name]...<>)."""
    style_name: str
    children: List[Node] = field(default_factory=list)

@dataclass
class ImageNode(Node):
    """Represents an image (@img: ...)."""
    src: str
    alt: Optional[str] = None

@dataclass
class LinkNode(Node):
    """Represents a link (@link: ...)."""
    href: str
    text: Optional[str] = None
