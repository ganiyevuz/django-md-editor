from __future__ import annotations

from abc import ABC, abstractmethod
from html import escape


class BaseRenderer(ABC):
    @abstractmethod
    def render(self, markdown_text: str) -> str: ...


class DefaultRenderer(BaseRenderer):
    """Renders markdown using python-markdown if installed,
    otherwise returns escaped plaintext.

    python-markdown is NOT a package dependency.
    Users install their preferred library and configure a renderer.
    """

    def render(self, markdown_text: str) -> str:
        if not markdown_text:
            return ""
        try:
            import markdown

            return markdown.markdown(
                markdown_text,
                extensions=["extra", "codehilite", "toc"],
            )
        except ImportError:
            return escape(markdown_text)
