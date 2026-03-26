from html import escape


class BaseRenderer:
    def render(self, markdown_text: str) -> str:
        raise NotImplementedError


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
