# src/kiro_renderer/parser.py

from .nodes import (
    DocumentNode,
    HeadingNode,
    HorizontalRuleNode,
    ParagraphNode,
    TextNode
)

class KiroParser:
    def __init__(self, text: str):
        self.lines = text.splitlines()
        self.document = DocumentNode()

    def parse(self) -> DocumentNode:
        """Parses the entire document text into an AST."""
        
        current_paragraph_lines = []

        for line in self.lines:
            # 1. Check for Block elements first (e.g., Headings, HRs)
            # This is a simplified check for Phase 1
            if line.startswith('#'):
                self._flush_paragraph(current_paragraph_lines)
                self._parse_heading(line)
                continue
            
            if line.strip() == '---':
                self._flush_paragraph(current_paragraph_lines)
                self.document.children.append(HorizontalRuleNode())
                continue

            # 2. If it's not a special block, treat it as part of a paragraph
            current_paragraph_lines.append(line)

        # Don't forget to process the last paragraph
        self._flush_paragraph(current_paragraph_lines)

        return self.document

    def _flush_paragraph(self, lines):
        """Processes collected lines into a ParagraphNode."""
        if lines:
            # For now, we join lines and create a single text node.
            # Inline parsing will happen here in a later phase.
            full_text = " ".join(lines)
            paragraph = ParagraphNode()
            paragraph.children.append(TextNode(text=full_text))
            self.document.children.append(paragraph)
            lines.clear()

    def _parse_heading(self, line):
        """Parses a heading line."""
        level = 0
        while line[level] == '#':
            level += 1
        
        # For now, we treat the rest of the line as simple text.
        # Inline parsing will be added later.
        text_content = line[level:].strip()
        heading = HeadingNode(level=level)
        heading.children.append(TextNode(text=text_content))
        self.document.children.append(heading)


def render(text: str) -> str:
    """The main entry point for rendering Kiro text to HTML."""
    parser = KiroParser(text)
    ast = parser.parse()
    
    # Note: For Phase 1, we are not implementing the HTML renderer yet.
    # We will return a simple string representation of the AST for now.
    return str(ast)