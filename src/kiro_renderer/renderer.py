from dataclasses import dataclass
from typing import List, Any, Tuple

from .nodes import (
    DocumentNode,
    ParagraphNode,
    HeadingNode,
    HorizontalRuleNode,
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
    Node,
    StyleDefinition
)

class KiroRenderer:
    def render(self, ast: DocumentNode) -> Tuple[str, str]:
        """Renders the given AST into an HTML string and a CSS string."""
        html_body_parts = []
        
        for child in ast.children:
            html_body_parts.append(self._render_node(child))
        
        # Render footnotes at the end
        if ast.footnotes:
            html_body_parts.append("<section class=\"kiro-footnotes\">\n")
            html_body_parts.append("<h2>Footnotes</h2>\n")
            html_body_parts.append("<ol>\n")
            # Sort by ID for consistent output, assuming IDs are sortable (e.g., numerical)
            sorted_footnote_ids = sorted(ast.footnotes.keys(), key=lambda x: int(x) if x.isdigit() else x)
            for footnote_id in sorted_footnote_ids:
                footnote_node = ast.footnotes[footnote_id]
                html_body_parts.append(f"<li id=\"fn-{footnote_id}\">")
                html_body_parts.append(self._render_children(footnote_node.children))
                html_body_parts.append(f" <a href=\"#fnref-{footnote_id}\" class=\"kiro-footnote-backref\">↩</a>")
                html_body_parts.append("</li>\n")
            html_body_parts.append("</ol>\n")
            html_body_parts.append("</section>\n")

        html_body_content = "".join(html_body_parts)
        css_content = self._generate_css(ast.styles)

        full_html = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Kiro Document</title>
    <link rel=\"stylesheet\" href=\"output.css\">
</head>
<body>
{html_body_content}
</body>
</html>"""

        return full_html, css_content

    def _generate_css(self, styles: dict) -> str:
        css_parts = []
        for style_name, style_def in styles.items():
            if style_def.is_global:
                selector = ":root"
            else:
                selector = f".kiro-{style_def.name}"
            
            rules = []
            if 'color' in style_def.properties:
                rules.append(f"  color: {style_def.properties['color']};")
            if 'font' in style_def.properties:
                rules.append(f"  font-family: '{style_def.properties['font']}';")
            if 'tailwind' in style_def.properties:
                # Tailwind classes are handled by external CSS framework, not directly here
                # This part might need more sophisticated handling if Tailwind is to be integrated directly
                pass 
            
            if rules:
                css_parts.append(f"{selector} {{\n" + "\n".join(rules) + "\n}}")
        return "\n".join(css_parts)

    def _render_node(self, node: Node) -> str:
        """Dispatches rendering based on node type."""
        if isinstance(node, DocumentNode):
            # DocumentNode is handled by the render method itself, not recursively here
            return ""
        elif isinstance(node, ParagraphNode):
            return self._render_paragraph(node)
        elif isinstance(node, HeadingNode):
            return self._render_heading(node)
        elif isinstance(node, HorizontalRuleNode):
            return self._render_horizontal_rule(node)
        elif isinstance(node, TextNode):
            return self._render_text(node)
        elif isinstance(node, CodeBlockNode):
            return self._render_code_block(node)
        elif isinstance(node, QuoteNode):
            return self._render_quote_block(node)
        elif isinstance(node, ListItemNode):
            return self._render_list_item(node)
        elif isinstance(node, OrderedListItemNode):
            return self._render_ordered_list_item(node)
        elif isinstance(node, ToggleNode):
            return self._render_toggle_block(node)
        elif isinstance(node, FootnoteDefinitionNode):
            # Footnote definitions are rendered at the end of the document
            return ""
        elif isinstance(node, StyleBlockNode):
            # Style blocks are handled by the parser and _generate_css method
            return ""
        elif isinstance(node, BoldNode):
            return self._render_bold(node)
        elif isinstance(node, EmphasisNode):
            return self._render_emphasis(node)
        elif isinstance(node, StrikethroughNode):
            return self._render_strikethrough(node)
        elif isinstance(node, InlineCodeNode):
            return self._render_inline_code(node)
        elif isinstance(node, FootnoteRefNode):
            return self._render_footnote_ref(node)
        elif isinstance(node, StyleSpanNode):
            return self._render_style_span(node)
        elif isinstance(node, ImageNode):
            return self._render_image(node)
        elif isinstance(node, LinkNode):
            return self._render_link(node)
        elif isinstance(node, MacroNode):
            return self._render_macro(node)
        else:
            # This should not happen if all node types are handled
            raise ValueError(f"Unknown node type: {type(node)}")

    def _render_children(self, children: List[Node]) -> str:
        """Helper to render a list of child nodes."""
        return "".join(self._render_node(child) for child in children)

    def _render_paragraph(self, node: ParagraphNode) -> str:
        return f"<p>{self._render_children(node.children)}</p>"

    def _render_heading(self, node: HeadingNode) -> str:
        return f"<h{node.level}>{self._render_children(node.children)}</h{node.level}>"

    def _render_horizontal_rule(self, node: HorizontalRuleNode) -> str:
        return "<hr>"

    def _render_text(self, node: TextNode) -> str:
        # Basic HTML escaping for text content
        return node.text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def _render_code_block(self, node: CodeBlockNode) -> str:
        lang_attr = f' class=\"language-{node.language}\"' if node.language else ""
        # Basic HTML escaping for code content
        escaped_content = node.content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f'<pre><code{lang_attr}>{escaped_content}</code></pre>'

    def _render_quote_block(self, node: QuoteNode) -> str:
        return f"<blockquote>{self._render_children(node.children)}</blockquote>"

    def _render_list_item(self, node: ListItemNode) -> str:
        # This is a simplified rendering for now, as full list parsing is complex.
        # It assumes a flat list structure.
        return f"<li>{self._render_children(node.children)}</li>"

    def _render_ordered_list_item(self, node: OrderedListItemNode) -> str:
        # This is a simplified rendering for now.
        return f"<li class=\"kiro-report-list-item\">{node.prefix} {self._render_children(node.children)}</li>"

    def _render_toggle_block(self, node: ToggleNode) -> str:
        summary_html = self._render_children(node.summary)
        content_html = self._render_children(node.content)
        return f"<details><summary>{summary_html}</summary><div>{content_html}</div></details>"

    def _render_bold(self, node: BoldNode) -> str:
        return f"<strong>{self._render_children(node.children)}</strong>"

    def _render_emphasis(self, node: EmphasisNode) -> str:
        return f"<em>{self._render_children(node.children)}</em>"

    def _render_strikethrough(self, node: StrikethroughNode) -> str:
        return f"<s>{self._render_children(node.children)}</s>"

    def _render_inline_code(self, node: InlineCodeNode) -> str:
        # Basic HTML escaping for code content
        escaped_text = node.text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f"<code>{escaped_text}</code>"

    def _render_footnote_ref(self, node: FootnoteRefNode) -> str:
        return f'<sup><a href=\"#fn-{node.id}\" id=\"fnref-{node.id}\" class=\"kiro-footnote-ref\">{node.id}</a></sup>'

    def _render_style_span(self, node: StyleSpanNode) -> str:
        return f'<span class=\"kiro-{node.style_name}\">{self._render_children(node.children)}</span>'

    def _render_image(self, node: ImageNode) -> str:
        alt_attr = f' alt=\"{node.alt}\"' if node.alt else ''
        figcaption = f'<figcaption>{node.alt}</figcaption>' if node.alt else ''
        return f'<figure><img src=\"{node.src}\"{alt_attr}>{figcaption}</figure>'

    def _render_link(self, node: LinkNode) -> str:
        text = node.text if node.text else node.href
        return f'<a href=\"{node.href}\" class=\"kiro-link\">{text}</a>'

    def _render_macro(self, node: MacroNode) -> str:
        # This is a placeholder for actual macro rendering logic.
        # For now, it will render a simple div with macro info.
        # In a real scenario, this would involve specific logic for each macro type (e.g., YouTube embed).
        args_str = ", ".join(node.args)
        return f'<div class=\"kiro-macro kiro-macro-{node.name}\">Macro: {node.name}({args_str})</div>'

    def _render_node(self, node: Node) -> str:
        """Dispatches rendering based on node type."""
        if isinstance(node, DocumentNode):
            return self.render(node)
        elif isinstance(node, ParagraphNode):
            return self._render_paragraph(node)
        elif isinstance(node, HeadingNode):
            return self._render_heading(node)
        elif isinstance(node, HorizontalRuleNode):
            return self._render_horizontal_rule(node)
        elif isinstance(node, TextNode):
            return self._render_text(node)
        elif isinstance(node, CodeBlockNode):
            return self._render_code_block(node)
        elif isinstance(node, QuoteNode):
            return self._render_quote_block(node)
        elif isinstance(node, ListItemNode):
            return self._render_list_item(node)
        elif isinstance(node, OrderedListItemNode):
            return self._render_ordered_list_item(node)
        elif isinstance(node, ToggleNode):
            return self._render_toggle_block(node)
        elif isinstance(node, FootnoteDefinitionNode):
            # Footnote definitions are rendered at the end of the document
            return ""
        elif isinstance(node, StyleBlockNode):
            # Style blocks are handled at the document level
            return ""
        elif isinstance(node, BoldNode):
            return self._render_bold(node)
        elif isinstance(node, EmphasisNode):
            return self._render_emphasis(node)
        elif isinstance(node, StrikethroughNode):
            return self._render_strikethrough(node)
        elif isinstance(node, InlineCodeNode):
            return self._render_inline_code(node)
        elif isinstance(node, FootnoteRefNode):
            return self._render_footnote_ref(node)
        elif isinstance(node, StyleSpanNode):
            return self._render_style_span(node)
        elif isinstance(node, ImageNode):
            return self._render_image(node)
        elif isinstance(node, LinkNode):
            return self._render_link(node)
        elif isinstance(node, MacroNode):
            return self._render_macro(node)
        else:
            # This should not happen if all node types are handled
            raise ValueError(f"Unknown node type: {type(node)}")

    def _render_children(self, children: List[Node]) -> str:
        """Helper to render a list of child nodes."""
        return "".join(self._render_node(child) for child in children)

    def _render_paragraph(self, node: ParagraphNode) -> str:
        return f"<p>{self._render_children(node.children)}</p>"

    def _render_heading(self, node: HeadingNode) -> str:
        return f"<h{node.level}>{self._render_children(node.children)}</h{node.level}>"

    def _render_horizontal_rule(self, node: HorizontalRuleNode) -> str:
        return "<hr>"

    def _render_text(self, node: TextNode) -> str:
        # Basic HTML escaping for text content
        return node.text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def _render_code_block(self, node: CodeBlockNode) -> str:
        lang_attr = f' class="language-{node.language}"' if node.language else ""
        # Basic HTML escaping for code content
        escaped_content = node.content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f'<pre><code{lang_attr}>{escaped_content}</code></pre>'

    def _render_quote_block(self, node: QuoteNode) -> str:
        return f"<blockquote>{self._render_children(node.children)}</blockquote>"

    def _render_list_item(self, node: ListItemNode) -> str:
        # This is a simplified rendering for now, as full list parsing is complex.
        # It assumes a flat list structure.
        return f"<li>{self._render_children(node.children)}</li>"

    def _render_ordered_list_item(self, node: OrderedListItemNode) -> str:
        # This is a simplified rendering for now.
        return f"<li class=\"kiro-report-list-item\">{node.prefix} {self._render_children(node.children)}</li>"

    def _render_toggle_block(self, node: ToggleNode) -> str:
        summary_html = self._render_children(node.summary)
        content_html = self._render_children(node.content)
        return f"<details><summary>{summary_html}</summary><div>{content_html}</div></details>"

    def _render_bold(self, node: BoldNode) -> str:
        return f"<strong>{self._render_children(node.children)}</strong>"

    def _render_emphasis(self, node: EmphasisNode) -> str:
        return f"<em>{self._render_children(node.children)}</em>"

    def _render_strikethrough(self, node: StrikethroughNode) -> str:
        return f"<s>{self._render_children(node.children)}</s>"

    def _render_inline_code(self, node: InlineCodeNode) -> str:
        # Basic HTML escaping for code content
        escaped_text = node.text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f"<code>{escaped_text}</code>"

    def _render_footnote_ref(self, node: FootnoteRefNode) -> str:
        return f'<sup><a href="#fn-{node.id}" id="fnref-{node.id}" class="kiro-footnote-ref">{node.id}</a></sup>'

    def _render_style_span(self, node: StyleSpanNode) -> str:
        return f'<span class="kiro-{node.style_name}">{self._render_children(node.children)}</span>'

    def _render_image(self, node: ImageNode) -> str:
        alt_attr = f' alt="{node.alt}"' if node.alt else ''
        figcaption = f'<figcaption>{node.alt}</figcaption>' if node.alt else ''
        return f'<figure><img src="{node.src}"{alt_attr}>{figcaption}</figure>'

    def _render_link(self, node: LinkNode) -> str:
        text = node.text if node.text else node.href
        return f'<a href="{node.href}" class="kiro-link">{text}</a>'

    def _render_macro(self, node: MacroNode) -> str:
        # This is a placeholder for actual macro rendering logic.
        # For now, it will render a simple div with macro info.
        # In a real scenario, this would involve specific logic for each macro type (e.g., YouTube embed).
        args_str = ", ".join(node.args)
        return f'<div class="kiro-macro kiro-macro-{node.name}">Macro: {node.name}({args_str})</div>'