# Development

## Setup

```bash
git clone https://github.com/ganiyevuz/django-md-editor.git
cd django-md-editor

# Install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync --group dev
```

## Running Tests

```bash
# Run all tests
make test

# Run with coverage
make coverage

# Run a specific test file
python -m pytest tests/test_views.py -v
```

## Linting

```bash
# Check
make lint

# Auto-fix
make format
```

## Example App

The `example/` directory contains a working Django project:

```bash
cd example
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://localhost:8000/admin/` to see the editor in the Django admin.

## Project Structure

```
django-md-editor/
├── src/django_markdown_widget/          # Package source
│   ├── static/                    # CSS and JavaScript
│   ├── templates/                 # Widget HTML template
│   ├── templatetags/              # Template tag and filter
│   ├── management/commands/       # Management commands
│   ├── widgets.py                 # MarkdownEditorWidget
│   ├── renderers.py               # BaseRenderer, DefaultRenderer
│   ├── uploads.py                 # BaseUploadHandler, DefaultUploadHandler
│   ├── cleanup.py                 # Media cleanup utilities
│   ├── mixins.py                  # MarkdownCleanupMixin
│   ├── admin.py                   # MarkdownEditorAdminMixin
│   ├── views.py                   # Preview and upload views
│   ├── urls.py                    # URL routing
│   └── settings.py                # Configuration defaults
├── tests/                         # Test suite
├── example/                       # Example Django project
├── docs/                          # Documentation (mkdocs)
└── pyproject.toml                 # Project metadata
```

## Building Docs

```bash
uv sync --group docs
mkdocs serve     # local preview at http://127.0.0.1:8000
mkdocs build     # build static site to site/
```

## Release

```bash
make release v=0.1.0
```

This lints, tests, bumps the version, creates a git tag, and pushes. GitHub Actions handles PyPI publishing via trusted publishing.
