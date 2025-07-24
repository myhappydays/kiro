# src/kiro_renderer/nodes.py

from dataclasses import dataclass, field
from typing import List, Any

# --- Base Nodes ---

@dataclass
class Node:
    """The base class for all AST nodes."""
    pass

@dataclass
class DocumentNode(Node):
    """The root node of the document's AST."""
    children: List[Node] = field(default_factory=list)

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

# --- Inline Nodes ---

@dataclass
class TextNode(Node):
    """Represents plain text content."""
    text: str
