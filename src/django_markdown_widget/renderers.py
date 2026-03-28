from __future__ import annotations

import re
from abc import ABC, abstractmethod
from html import escape

# Simple HTML sanitizer — allows safe tags, strips everything else
_ALLOWED_TAGS = {
    "p", "br", "hr", "h1", "h2", "h3", "h4", "h5", "h6",
    "em", "strong", "del", "s", "mark", "sub", "sup",
    "ul", "ol", "li", "a", "img", "video", "source", "iframe",
    "pre", "code", "blockquote", "table", "thead", "tbody",
    "tr", "th", "td", "details", "summary",
    "input", "div", "span",
}
_ALLOWED_ATTRS = {
    "a": {"href", "title", "rel"},
    "img": {"src", "alt", "title", "width", "height"},
    "video": {
        "src", "controls", "autoplay", "muted", "loop", "width",
        "height", "controlslist", "disablepictureinpicture",
    },
    "source": {"src", "type"},
    "iframe": {
        "src", "width", "height", "frameborder", "allowfullscreen",
        "allow", "title", "referrerpolicy", "loading",
    },
    "input": {"type", "checked", "disabled"},
    "td": {"align"},
    "th": {"align"},
    "code": {"class"},
    "div": {"class"},
    "span": {"class"},
    "pre": {"class"},
}

_TAG_RE = re.compile(r"<(/?)(\w+)([^>]*)>", re.DOTALL)
_ATTR_RE = re.compile(r'(\w[\w-]*)(?:\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|(\S+)))?')


def _sanitize_html(html: str) -> str:
    """Strip disallowed tags and attributes from HTML."""
    def replace_tag(match):
        closing, tag, attrs_str = match.group(1), match.group(2).lower(), match.group(3)
        if tag not in _ALLOWED_TAGS:
            return ""
        if closing:
            return f"</{tag}>"
        allowed = _ALLOWED_ATTRS.get(tag, set())
        safe_attrs = []
        for attr_match in _ATTR_RE.finditer(attrs_str):
            attr_name = attr_match.group(1).lower()
            if attr_name not in allowed:
                continue
            attr_val = (
                attr_match.group(2)
                or attr_match.group(3)
                or attr_match.group(4)
                or ""
            )
            # Block javascript: URLs
            val_lower = attr_val.strip().lower()
            if attr_name in ("href", "src") and val_lower.startswith("javascript:"):
                continue
            safe_attrs.append(f'{attr_name}="{escape(attr_val)}"')
        attrs = (" " + " ".join(safe_attrs)) if safe_attrs else ""
        return f"<{tag}{attrs}>"

    # Strip <script>, <style>, <iframe>, <object>, <embed> and their content
    html = re.sub(
        r"<(script|style|iframe|object|embed)[^>]*>.*?</\1>",
        "", html, flags=re.DOTALL | re.IGNORECASE,
    )
    return _TAG_RE.sub(replace_tag, html)


class BaseRenderer(ABC):
    @abstractmethod
    def render(self, markdown_text: str) -> str: ...


class DefaultRenderer(BaseRenderer):
    """Renders markdown using python-markdown if installed,
    otherwise returns escaped plaintext.

    python-markdown is NOT a package dependency.
    Users install their preferred library and configure a renderer.

    Output is sanitized to prevent XSS — only safe HTML tags and
    attributes are preserved.
    """

    def render(self, markdown_text: str) -> str:
        if not markdown_text:
            return ""
        try:
            import markdown

            html = markdown.markdown(
                markdown_text,
                extensions=["extra", "codehilite", "toc"],
            )
            return _sanitize_html(html)
        except ImportError:
            return escape(markdown_text)
