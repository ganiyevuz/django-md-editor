from django.forms import ModelForm

from django_md_editor.widgets import MarkdownEditorWidget
from posts.models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        widgets = {
            "content": MarkdownEditorWidget(),
        }
