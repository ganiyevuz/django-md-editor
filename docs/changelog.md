# Changelog

## 2.0.0

### Editor Modes
- Added **split (side-by-side) view** with live preview that updates as you type
- Three editor tabs: **Write**, **Split**, **Preview**
- **Draggable split divider** with grip handle -- resize panels from 20% to 80%
- Divider supports mouse and touch drag
- Split mode works in both normal and fullscreen

### Preview & Rendering
- Switched client-side renderer from marked.js to **markdown-it** with official plugins
- Bundled plugins: `markdown-it-mark`, `markdown-it-sub`, `markdown-it-sup`, `markdown-it-task-lists`
- Added **syntax highlighting** for code blocks via highlight.js (GitHub light + dark themes)
- Preview is now **fully client-side** -- no server round-trip needed
- `==highlight==` renders as `<mark>`, `^super^` as `<sup>`, `~sub~` as `<sub>`
- Task lists render as interactive checkboxes
- Removed server-side preview endpoint (`PreviewView`, `/preview` URL)
- Removed `preview_url` widget parameter and `CLIENT_RENDERER` setting

### Media Uploads
- **Image, video, and document uploads** with dedicated toolbar buttons
- Upload type auto-detection: images insert `![](url)`, videos insert `<video>`, documents insert `[name](url)`
- Video uploads prompt for autoplay option, disable download controls
- Default allowed types expanded: images, videos (mp4/webm/ogg), documents (pdf, docx, xlsx, pptx, zip, csv, json, txt)
- Max upload size increased to **50 MB**
- **Temp upload system**: files upload to `md-editor/tmp/`, finalize to permanent storage on form submit
- New `/finalize` endpoint moves referenced temp files, unreferenced files cleaned by management command
- New settings: `TEMP_UPLOAD_PATH`, `TEMP_MAX_AGE`

### Embed Support
- New **embed toolbar button** -- paste a URL or raw `<iframe>` embed code
- Auto-detects **YouTube**, **Vimeo**, **CodePen** URLs and generates proper embeds
- Pasting YouTube's own embed code works directly
- `iframe` added to both client and server sanitizer allowlists

### Autosave
- **Autosave to browser localStorage** -- drafts survive page reloads
- Debounced save (500ms after typing stops)
- **Toggle switch** in tabs bar to enable/disable autosave
- Footer shows save status: "Saving...", "Saved at 2:31 PM", "Draft from 2:30 PM"
- Auto-restores drafts on page load (only if textarea is empty or unchanged)
- Drafts expire after 7 days and clear on form submit

### UI Improvements
- Moved **fullscreen button** from toolbar to tabs bar (top right)
- Added **styled tooltips** on all toolbar buttons (appear below on hover)
- **Toast notifications** for upload errors (replaces `alert()`)
- Toolbar buttons use `aria-label` for accessibility
- Toolbar **regrouped by purpose**: formatting, structure, code, lists, media, blocks, extras, actions

### Undo/Redo
- **Custom undo/redo history stack** (100 states)
- `Ctrl+Z` / `Cmd+Z` to undo, `Ctrl+Shift+Z` / `Cmd+Shift+Z` to redo
- Both keyboard shortcuts and toolbar buttons work correctly

### Security
- **HTML sanitizer** on both client and server side
- Server-side `DefaultRenderer` strips `<script>`, `<style>`, `<iframe>` (except allowed), event handlers, and `javascript:` URLs
- Client-side sanitizer runs after markdown-it render
- **Path traversal protection** in cleanup module (`posixpath.normpath`, rejects `..`)
- **Filename sanitization** -- strips path components, unsafe characters, enforces 200-char limit
- **Explicit CSRF protection** via `@method_decorator(csrf_protect)` on all views
- HTML-escaped `url` and `name` in video/embed tag generation
- Removed `image/svg+xml` from default allowed upload types (XSS risk)
- `</script>` escaping in toolbar JSON output

### Bug Fixes
- Fixed all toolbar actions not working due to `handleAction` scope issue
- Fixed split mode editor showing white space below textarea
- Fixed split divider not working in fullscreen mode
- Fixed `overflow: hidden` on container clipping tooltips
- Removed deprecated `document.execCommand("undo/redo")` calls
- Removed redundant "attach" button (covered by image/video/document)
- Removed "mention" and "ref" buttons (require backend, not useful standalone)

### Other
- Added screenshots to README and docs
- Updated example showcase with all current features
- 78 tests passing

## 1.0.1

- Modernized base classes with `abc.ABC` and `@abstractmethod`
- Added `from __future__ import annotations` across all modules
- DRYed up view auth check into `AuthRequiredMixin`
- Catch `ValidationError` specifically instead of bare `Exception` in upload view
- Added `markdown` template filter (`{{ text|markdown }}`) alongside existing tag
- Added `MarkdownCleanupMixin` for automatic orphaned media deletion on model save
- Added `cleanup_markdown_media` management command for bulk orphan detection
- Added `extract_media_urls()` and `delete_orphaned_media()` utility functions
- Added `CLEANUP_MEDIA` setting (opt-in, defaults to `False`)
- Added type hints for upload handler methods (`UploadedFile`)
- Added return type hint for `get_setting()`
- Removed deprecated `default_app_config` (unnecessary since Django 3.2)
- Added mkdocs documentation site with Material theme
- Updated README with full usage guide
- Test coverage at 95%+ (82 tests)

## 1.0.0

Initial release.

- GitHub-style markdown editor widget for Django forms
- Django admin integration via `MarkdownEditorAdminMixin`
- Pluggable renderer and upload handler architecture
- `DefaultRenderer` with python-markdown (optional dependency)
- `DefaultUploadHandler` with Django's `default_storage`
- Template tag (`{% markdown %}`) for rendering markdown in templates
- Image/file upload with drag & drop and paste support
- Toolbar with headings, formatting, lists, tables, code blocks, and more
- Light, dark, and auto theme support
- Keyboard shortcuts (Ctrl+B, Ctrl+I, Ctrl+K, etc.)
- Full test suite with pytest
