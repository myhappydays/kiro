import re
from typing import List, Optional

from .nodes import (
    DocumentNode,
    HeadingNode,
    HorizontalRuleNode,
    ParagraphNode,
    TextNode,
    CodeBlockNode,
    QuoteNode,
    ListItemNode,
    OrderedListItemNode,
    ToggleNode,
    StyleBlockNode,
    FootnoteDefinitionNode,
    BoldNode,
    EmphasisNode,
    StrikethroughNode,
    InlineCodeNode,
    FootnoteRefNode,
    StyleSpanNode,
    ImageNode,
    LinkNode,
    MacroNode,
    Node
)

class KiroParser:
    def __init__(self, text: str):
        self.lines = text.splitlines()
        self.document = DocumentNode()
        self.current_line_idx = 0

    def parse(self) -> DocumentNode:
        """Parses the entire document text into an AST."""
        while self.current_line_idx < len(self.lines):
            line = self.lines[self.current_line_idx]

            # Skip empty lines at the beginning of a block
            if not line.strip():
                self.current_line_idx += 1
                continue

            # Try to parse block elements in order of precedence
            if self._parse_style_block():
                continue
            if self._parse_code_block():
                continue
            if self._parse_heading():
                continue
            if self._parse_horizontal_rule():
                continue
            if self._parse_quote_block():
                continue
            if self._parse_toggle_block():
                continue
            if self._parse_list_block():
                continue
            if self._parse_footnote_definition():
                continue
            if self._parse_image_or_link_block():
                continue
            if self._parse_macro():
                continue

            # If no special block, treat as paragraph
            self._parse_paragraph()

        return self.document

    def _get_current_line(self) -> str:
        if self.current_line_idx < len(self.lines):
            return self.lines[self.current_line_idx]
        return ""

    def _advance_line(self):
        self.current_line_idx += 1

    def _parse_style_block(self) -> bool:
        line = self._get_current_line()
        if line.strip() == '<style>':
            self._advance_line()
            style_content_lines = []
            while self.current_line_idx < len(self.lines):
                current_line = self._get_current_line()
                if re.match(r'^<>$', current_line.strip()): # Use regex for exact match
                    self._advance_line()
                    break
                style_content_lines.append(current_line)
                self._advance_line()
            
            self.document.styles['main'] = "\n".join(style_content_lines)
            return True
        return False

    def _parse_code_block(self) -> bool:
        line = self._get_current_line()
        match = re.match(r'^```(\S*)$', line.strip())
        if match:
            self._advance_line()
            language = match.group(1) if match.group(1) else None
            code_content_lines = []
            while self.current_line_idx < len(self.lines):
                current_line = self._get_current_line()
                if current_line.strip() == '```':
                    self._advance_line()
                    break
                code_content_lines.append(current_line)
                self._advance_line()
            self.document.children.append(CodeBlockNode(language=language, content="\n".join(code_content_lines)))
            return True
        return False

    def _parse_heading(self) -> bool:
        line = self._get_current_line()
        match = re.match(r'^(#+)\s*(.*)$', line)
        if match:
            level = len(match.group(1))
            text_content = match.group(2).strip()
            heading = HeadingNode(level=level)
            heading.children.extend(self._parse_inlines(text_content)) # Apply inline parsing
            self.document.children.append(heading)
            self._advance_line()
            return True
        return False

    def _parse_horizontal_rule(self) -> bool:
        line = self._get_current_line()
        if line.strip() == '---':
            self.document.children.append(HorizontalRuleNode())
            self._advance_line()
            return True
        return False

    def _parse_quote_block(self) -> bool:
        line = self._get_current_line()
        if line.startswith('|'):
            quote_lines = []
            while self.current_line_idx < len(self.lines) and self._get_current_line().startswith('|'):
                quote_lines.append(self._get_current_line()[1:].strip())
                self._advance_line()
            
            quote_node = QuoteNode()
            # Recursively parse content within the quote block
            # For simplicity, treating as a single paragraph for now, but can be extended.
            paragraph = ParagraphNode()
            paragraph.children.extend(self._parse_inlines(" ".join(quote_lines))) # Apply inline parsing
            quote_node.children.append(paragraph)
            self.document.children.append(quote_node)
            return True
        return False

    def _parse_toggle_block(self) -> bool:
        line = self._get_current_line()
        if line.startswith('>'):
            summary_text = line[1:].strip()
            toggle_node = ToggleNode()
            toggle_node.summary.extend(self._parse_inlines(summary_text)) # Apply inline parsing
            self._advance_line()

            content_lines = []
            while self.current_line_idx < len(self.lines):
                current_line = self._get_current_line()
                if current_line.startswith('>>'):
                    content_lines.append(current_line[2:].strip())
                    self._advance_line()
                elif not current_line.strip(): # Allow blank lines within toggle content
                    content_lines.append("")
                    self._advance_line()
                else:
                    break
            
            if content_lines:
                paragraph = ParagraphNode()
                paragraph.children.extend(self._parse_inlines(" ".join(content_lines))) # Apply inline parsing
                toggle_node.content.append(paragraph)
            
            self.document.children.append(toggle_node)
            return True
        return False

    def _parse_list_block(self) -> bool:
        # This is a simplified placeholder. Full list parsing is complex.
        line = self._get_current_line()
        if re.match(r'^[-*+]\s', line) or re.match(r'^-(\d+\.)([A-Za-z]\.)*\s', line):
            list_item_text = line[line.find(' '):].strip()
            list_item_node = ListItemNode() # Or OrderedListItemNode
            paragraph = ParagraphNode()
            paragraph.children.extend(self._parse_inlines(list_item_text)) # Apply inline parsing
            list_item_node.children.append(paragraph)
            self.document.children.append(list_item_node)
            self._advance_line()
            return True
        return False

    def _parse_footnote_definition(self) -> bool:
        line = self._get_current_line()
        match = re.match(r'^\[\^([a-zA-Z0-9_\-]+)\]:\s*(.*)$', line)
        if match:
            footnote_id = match.group(1)
            content_text = match.group(2).strip()
            footnote_node = FootnoteDefinitionNode(id=footnote_id)
            paragraph = ParagraphNode()
            paragraph.children.extend(self._parse_inlines(content_text)) # Apply inline parsing
            footnote_node.children.append(paragraph)
            self.document.footnotes[footnote_id] = footnote_node
            self.document.children.append(footnote_node) # Also add to children for rendering order
            self._advance_line()
            return True
        return False

    def _parse_image_or_link_block(self) -> bool:
        line = self._get_current_line()
        # Image: @img: path/to/image.png (description)
        img_match = re.match(r'^@img:\s*(\S+)(?:\s*\((.*)\))?$', line)
        if img_match:
            src = img_match.group(1)
            alt = img_match.group(2) if img_match.group(2) else None
            self.document.children.append(ImageNode(src=src, alt=alt))
            self._advance_line()
            return True
        
        # Link: @link: https://example.com (description)
        link_match = re.match(r'^@link:\s*(\S+)(?:\s*\((.*)\))?$', line)
        if link_match:
            href = link_match.group(1)
            text = link_match.group(2) if link_match.group(2) else None
            self.document.children.append(LinkNode(href=href, text=text))
            self._advance_line()
            return True
        return False

    def _parse_macro(self) -> bool:
        line = self._get_current_line()
        # Macro: !macro_name(arg1, arg2, ...)
        macro_match = re.match(r'^!([a-zA-Z_][a-zA-Z0-9_]*)\((.*)\)$', line)
        if macro_match:
            macro_name = macro_match.group(1)
            args_str = macro_match.group(2)
            args = [arg.strip() for arg in args_str.split(',')] if args_str else []
            self.document.children.append(MacroNode(name=macro_name, args=args))
            self._advance_line()
            return True
        return False

    def _parse_paragraph(self):
        current_paragraph_lines = []
        while self.current_line_idx < len(self.lines):
            line = self._get_current_line()
            # If it's an empty line or a new block element starts, end paragraph
            if not line.strip() or \
               re.match(r'^(#+)\s*(.*)$', line) or \
               line.strip() == '---' or \
               line.startswith('|') or \
               line.startswith('>') or \
               re.match(r'^```(\S*)$', line.strip()) or \
               re.match(r'^[-*+]\s', line) or \
               re.match(r'^-(\d+\.)([A-Za-z]\.)*\s', line) or \
               re.match(r'^\[\^([a-zA-Z0-9_\-]+)\]:\s*(.*)$', line) or \
               re.match(r'^@img:\s*(\S+)(?:\s*\((.*)\))?$', line) or \
               re.match(r'^@link:\s*(\S+)(?:\s*\((.*)\))?$', line) or \
               re.match(r'^!([a-zA-Z_][a-zA-Z0-9_]*)\((.*)\)$', line) or \
               line.strip() == '<style>':
                break
            current_paragraph_lines.append(line)
            self._advance_line()
        
        if current_paragraph_lines:
            paragraph = ParagraphNode()
            paragraph.children.extend(self._parse_inlines(" ".join(current_paragraph_lines))) # Apply inline parsing
            self.document.children.append(paragraph)

    def _parse_inlines(self, text: str) -> List[Node]:
        nodes = []
        i = 0
        while i < len(text):
            # Escape character
            if text[i] == '\\':
                if i + 1 < len(text):
                    nodes.append(TextNode(text=text[i+1]))
                    i += 2
                    continue
                else:
                    nodes.append(TextNode(text='\\'))
                    i += 1
                    continue

            # Bold (**...**)
            match = re.match(r'^\*\*(.+?)\*\*', text[i:])
            if match:
                nodes.append(BoldNode(children=self._parse_inlines(match.group(1))))
                i += match.end()
                continue

            # Emphasis (*...*)
            match = re.match(r'^\*(.+?)\*', text[i:])
            if match:
                nodes.append(EmphasisNode(children=self._parse_inlines(match.group(1))))
                i += match.end()
                continue

            # Strikethrough (~~...~~)
            match = re.match(r'^~~(.+?)~~', text[i:])
            if match:
                nodes.append(StrikethroughNode(children=self._parse_inlines(match.group(1))))
                i += match.end()
                continue

            # Inline Code (`...`)
            match = re.match(r'^`(.+?)`', text[i:])
            if match:
                nodes.append(InlineCodeNode(text=match.group(1)))
                i += match.end()
                continue

            # Footnote Reference ([^id])
            match = re.match(r'^\^\[([a-zA-Z0-9_\-]+)\]', text[i:])
            if match:
                nodes.append(FootnoteRefNode(id=match.group(1)))
                i += match.end()
                continue

            # Style Span ([name]...<>)
            match = re.match(r'^\[([a-zA-Z0-9_\-]+)\](.+?)<>', text[i:])
            if match:
                style_name = match.group(1)
                content = match.group(2)
                nodes.append(StyleSpanNode(style_name=style_name, children=self._parse_inlines(content)))
                i += match.end()
                continue

            # If no match, just add the character as a TextNode
            nodes.append(TextNode(text=text[i]))
            i += 1
        return nodes
