(function () {
  "use strict";

  // ---------------------------------------------------------------------------
  // 1. TOOLBAR_BUTTONS
  // ---------------------------------------------------------------------------
  const TOOLBAR_BUTTONS = {
    heading: { icon: "H", title: "Heading", action: "heading" },
    bold: { icon: "B", title: "Bold (Ctrl+B)", action: "bold", style: "font-weight:bold" },
    italic: { icon: "I", title: "Italic (Ctrl+I)", action: "italic", style: "font-style:italic" },
    quote: { icon: "\u201C\u201D", title: "Quote (Ctrl+Shift+.)", action: "quote" },
    code: { icon: "&lt;/&gt;", title: "Code (Ctrl+E)", action: "code" },
    link: { icon: "\uD83D\uDD17", title: "Link (Ctrl+K)", action: "link" },
    "ordered-list": { icon: "1.", title: "Ordered List (Ctrl+Shift+7)", action: "ordered-list" },
    "unordered-list": { icon: "\u2022", title: "Unordered List (Ctrl+Shift+8)", action: "unordered-list" },
    "task-list": { icon: "\u2611", title: "Task List", action: "task-list" },
    attach: { icon: "\uD83D\uDCCE", title: "Attach File", action: "attach" },
    mention: { icon: "@", title: "Mention", action: "mention" },
    ref: { icon: "#", title: "Reference", action: "ref" },
    undo: { icon: "\u21A9", title: "Undo (Ctrl+Z)", action: "undo", align: "right" },
    redo: { icon: "\u21AA", title: "Redo (Ctrl+Shift+Z)", action: "redo", align: "right" },
    fullscreen: { icon: "\u26F6", title: "Fullscreen", action: "fullscreen", align: "right" },
    separator: { type: "separator" },
  };

  // ---------------------------------------------------------------------------
  // 2. initEditor(container)
  // ---------------------------------------------------------------------------
  function initEditor(container) {
    let toolbarConfig;
    var configScript = container.querySelector(".md-editor-config");
    try {
      toolbarConfig = JSON.parse(configScript ? configScript.textContent : "[]");
    } catch (e) {
      toolbarConfig = Object.keys(TOOLBAR_BUTTONS);
    }
    if (!toolbarConfig.length) {
      toolbarConfig = Object.keys(TOOLBAR_BUTTONS);
    }
    const previewUrl = container.dataset.previewUrl || "";
    const uploadUrl = container.dataset.uploadUrl || "";

    const textarea = container.querySelector(".md-editor-textarea");
    const toolbar = container.querySelector(".md-editor-toolbar");
    const tabs = container.querySelectorAll(".md-editor-tab");
    const writePanels = container.querySelectorAll(".md-editor-write");
    const previewPanels = container.querySelectorAll(".md-editor-preview");
    const fileInput = container.querySelector(".md-editor-file-input");
    const footerUpload = container.querySelector(".md-editor-footer-upload");

    if (!textarea || !toolbar) return;

    // Build toolbar buttons
    let spacerInserted = false;
    toolbarConfig.forEach((name) => {
      const def = TOOLBAR_BUTTONS[name];
      if (!def) return;

      if (def.type === "separator") {
        const sep = document.createElement("span");
        sep.className = "md-editor-toolbar-separator";
        toolbar.appendChild(sep);
        return;
      }

      // Insert spacer before the first right-aligned button
      if (def.align === "right" && !spacerInserted) {
        const spacer = document.createElement("span");
        spacer.className = "md-editor-toolbar-spacer";
        spacer.style.flex = "1";
        toolbar.appendChild(spacer);
        spacerInserted = true;
      }

      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "md-editor-toolbar-btn";
      btn.title = def.title;
      btn.dataset.action = def.action;
      btn.innerHTML = def.icon;
      if (def.style) btn.style.cssText = def.style;

      btn.addEventListener("click", function () {
        handleAction(def.action, textarea, container, fileInput, uploadUrl);
        textarea.focus();
      });

      toolbar.appendChild(btn);
    });

    // Wire tab switching
    tabs.forEach((tab) => {
      tab.addEventListener("click", function () {
        const targetTab = this.dataset.tab;

        tabs.forEach((t) => t.classList.remove("md-editor-tab--active"));
        this.classList.add("md-editor-tab--active");

        if (targetTab === "preview") {
          writePanels.forEach((p) => {
            p.classList.add("md-editor-panel--hidden");
            p.classList.remove("md-editor-panel--active");
          });
          previewPanels.forEach((p) => {
            p.classList.remove("md-editor-panel--hidden");
            p.classList.add("md-editor-panel--active");
          });
          toolbar.style.display = "none";

          const previewContent = container.querySelector(".md-editor-preview-content");
          if (previewContent) {
            renderPreview(textarea.value, previewContent, previewUrl);
          }
        } else {
          previewPanels.forEach((p) => {
            p.classList.add("md-editor-panel--hidden");
            p.classList.remove("md-editor-panel--active");
          });
          writePanels.forEach((p) => {
            p.classList.remove("md-editor-panel--hidden");
            p.classList.add("md-editor-panel--active");
          });
          toolbar.style.display = "";
        }
      });
    });

    // Wire keyboard shortcuts on textarea
    textarea.addEventListener("keydown", function (e) {
      const ctrl = e.ctrlKey || e.metaKey;

      if (ctrl && !e.shiftKey && e.key === "b") {
        e.preventDefault();
        handleAction("bold", textarea, container, fileInput, uploadUrl);
      } else if (ctrl && !e.shiftKey && e.key === "i") {
        e.preventDefault();
        handleAction("italic", textarea, container, fileInput, uploadUrl);
      } else if (ctrl && !e.shiftKey && e.key === "k") {
        e.preventDefault();
        handleAction("link", textarea, container, fileInput, uploadUrl);
      } else if (ctrl && !e.shiftKey && e.key === "e") {
        e.preventDefault();
        handleAction("code", textarea, container, fileInput, uploadUrl);
      } else if (ctrl && e.shiftKey && (e.key === ">" || e.key === ".")) {
        e.preventDefault();
        handleAction("quote", textarea, container, fileInput, uploadUrl);
      } else if (ctrl && e.shiftKey && e.key === "7") {
        e.preventDefault();
        handleAction("ordered-list", textarea, container, fileInput, uploadUrl);
      } else if (ctrl && e.shiftKey && e.key === "8") {
        e.preventDefault();
        handleAction("unordered-list", textarea, container, fileInput, uploadUrl);
      } else if (e.key === "Escape") {
        if (container.classList.contains("md-editor--fullscreen")) {
          container.classList.remove("md-editor--fullscreen");
        }
      }
    });

    // Wire drag/drop file handling
    container.addEventListener("dragover", function (e) {
      e.preventDefault();
      container.classList.add("md-editor--dragover");
    });

    container.addEventListener("dragleave", function (e) {
      if (!container.contains(e.relatedTarget)) {
        container.classList.remove("md-editor--dragover");
      }
    });

    container.addEventListener("drop", function (e) {
      e.preventDefault();
      container.classList.remove("md-editor--dragover");
      if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0) {
        uploadFiles(e.dataTransfer.files, textarea, uploadUrl);
      }
    });

    // Wire paste file handling
    textarea.addEventListener("paste", function (e) {
      if (!e.clipboardData || !e.clipboardData.files || e.clipboardData.files.length === 0) return;
      const imageFiles = Array.from(e.clipboardData.files).filter((f) => f.type.startsWith("image/"));
      if (imageFiles.length > 0) {
        e.preventDefault();
        uploadFiles(imageFiles, textarea, uploadUrl);
      }
    });

    // Wire file input (hidden) change
    if (fileInput) {
      fileInput.addEventListener("change", function () {
        if (fileInput.files && fileInput.files.length > 0) {
          uploadFiles(fileInput.files, textarea, uploadUrl);
          fileInput.value = "";
        }
      });
    }

    // Wire footer upload click
    if (footerUpload && fileInput) {
      footerUpload.addEventListener("click", function () {
        fileInput.click();
      });
    }
  }

  // ---------------------------------------------------------------------------
  // 3. handleAction
  // ---------------------------------------------------------------------------
  function handleAction(action, textarea, container, fileInput, uploadUrl) {
    switch (action) {
      case "heading":
        wrapLines(textarea, "# ");
        break;
      case "bold":
        wrapSelection(textarea, "**", "**");
        break;
      case "italic":
        wrapSelection(textarea, "_", "_");
        break;
      case "quote":
        wrapLines(textarea, "> ");
        break;
      case "code":
        toggleCode(textarea);
        break;
      case "link":
        insertLink(textarea);
        break;
      case "ordered-list":
        wrapLines(textarea, "1. ");
        break;
      case "unordered-list":
        wrapLines(textarea, "- ");
        break;
      case "task-list":
        wrapLines(textarea, "- [ ] ");
        break;
      case "attach":
        if (fileInput) fileInput.click();
        break;
      case "mention":
        insertAtCursor(textarea, "@");
        break;
      case "ref":
        insertAtCursor(textarea, "#");
        break;
      case "undo":
        document.execCommand("undo");
        break;
      case "redo":
        document.execCommand("redo");
        break;
      case "fullscreen":
        container.classList.toggle("md-editor--fullscreen");
        break;
      default:
        break;
    }
  }

  // ---------------------------------------------------------------------------
  // 4. Text manipulation helpers
  // ---------------------------------------------------------------------------

  function wrapSelection(textarea, before, after) {
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const value = textarea.value;
    const selected = value.substring(start, end);

    // Toggle off if already wrapped
    const beforeLen = before.length;
    const afterLen = after.length;
    if (
      start >= beforeLen &&
      value.substring(start - beforeLen, start) === before &&
      value.substring(end, end + afterLen) === after
    ) {
      const newValue =
        value.substring(0, start - beforeLen) +
        selected +
        value.substring(end + afterLen);
      textarea.value = newValue;
      textarea.selectionStart = start - beforeLen;
      textarea.selectionEnd = end - beforeLen;
      triggerInput(textarea);
      return;
    }

    const text = selected || "text";
    const newValue = value.substring(0, start) + before + text + after + value.substring(end);
    textarea.value = newValue;

    if (selected) {
      textarea.selectionStart = start + beforeLen;
      textarea.selectionEnd = end + beforeLen;
    } else {
      textarea.selectionStart = start + beforeLen;
      textarea.selectionEnd = start + beforeLen + text.length;
    }
    triggerInput(textarea);
  }

  function wrapLines(textarea, prefix) {
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const value = textarea.value;

    // Find the start of the first selected line
    const lineStart = value.lastIndexOf("\n", start - 1) + 1;
    // Find the end of the last selected line
    let lineEnd = value.indexOf("\n", end);
    if (lineEnd === -1) lineEnd = value.length;

    const selectedBlock = value.substring(lineStart, lineEnd);
    const lines = selectedBlock.split("\n");

    const allPrefixed = lines.every((line) => line.startsWith(prefix));

    let newBlock;
    if (allPrefixed) {
      // Toggle off
      newBlock = lines.map((line) => line.substring(prefix.length)).join("\n");
    } else {
      newBlock = lines.map((line) => (line.startsWith(prefix) ? line : prefix + line)).join("\n");
    }

    textarea.value = value.substring(0, lineStart) + newBlock + value.substring(lineEnd);
    textarea.selectionStart = lineStart;
    textarea.selectionEnd = lineStart + newBlock.length;
    triggerInput(textarea);
  }

  function toggleCode(textarea) {
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const value = textarea.value;
    const selected = value.substring(start, end);

    if (selected.includes("\n")) {
      // Multi-line: use code fence
      const fence = "```";
      // Toggle off
      if (
        start >= fence.length + 1 &&
        value.substring(start - fence.length - 1, start) === fence + "\n" &&
        value.substring(end, end + fence.length + 1) === "\n" + fence
      ) {
        const newValue =
          value.substring(0, start - fence.length - 1) +
          selected +
          value.substring(end + fence.length + 1);
        textarea.value = newValue;
        textarea.selectionStart = start - fence.length - 1;
        textarea.selectionEnd = end - fence.length - 1;
      } else {
        const newValue =
          value.substring(0, start) + fence + "\n" + selected + "\n" + fence + value.substring(end);
        textarea.value = newValue;
        textarea.selectionStart = start + fence.length + 1;
        textarea.selectionEnd = end + fence.length + 1;
      }
    } else {
      // Single-line or no selection: inline backtick
      wrapSelection(textarea, "`", "`");
      return;
    }
    triggerInput(textarea);
  }

  function insertLink(textarea) {
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const value = textarea.value;
    const selected = value.substring(start, end);

    if (selected) {
      // Selected text becomes link text
      const inserted = "[" + selected + "](url)";
      textarea.value = value.substring(0, start) + inserted + value.substring(end);
      // Place cursor on "url"
      const urlStart = start + selected.length + 3;
      textarea.selectionStart = urlStart;
      textarea.selectionEnd = urlStart + 3;
    } else {
      const inserted = "[text](url)";
      textarea.value = value.substring(0, start) + inserted + value.substring(end);
      // Select "text"
      textarea.selectionStart = start + 1;
      textarea.selectionEnd = start + 5;
    }
    triggerInput(textarea);
  }

  function insertAtCursor(textarea, text) {
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const value = textarea.value;
    textarea.value = value.substring(0, start) + text + value.substring(end);
    textarea.selectionStart = start + text.length;
    textarea.selectionEnd = start + text.length;
    triggerInput(textarea);
  }

  function triggerInput(textarea) {
    textarea.dispatchEvent(new Event("input", { bubbles: true }));
  }

  // ---------------------------------------------------------------------------
  // 5. renderPreview
  // ---------------------------------------------------------------------------
  function renderPreview(markdown, previewEl, serverUrl) {
    if (!markdown) {
      previewEl.innerHTML = "<p style='color:var(--md-text-muted)'>Nothing to preview</p>";
      return;
    }

    // Client-side render if marked is available
    var clientRendered = false;
    if (typeof marked !== "undefined" && typeof marked.parse === "function") {
      try {
        previewEl.innerHTML = marked.parse(markdown);
        clientRendered = true;
      } catch (e) {
        previewEl.textContent = markdown;
      }
    } else {
      previewEl.textContent = markdown;
    }

    // Server-side render if URL provided
    // Only replace client render if server returns actual HTML (contains tags)
    if (serverUrl) {
      fetch(serverUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({ text: markdown }),
      })
        .then(function (response) {
          if (!response.ok) throw new Error("Server error: " + response.status);
          return response.json();
        })
        .then(function (data) {
          var html = data && (data.html !== undefined ? data.html : data.content);
          if (html && (!clientRendered || /<[a-z][\s\S]*>/i.test(html))) {
            previewEl.innerHTML = html;
          }
        })
        .catch(function () {
          // Keep client-side render on failure; if no client render, show plain text
          if (!clientRendered) {
            previewEl.textContent = markdown;
          }
        });
    } else if (typeof marked === "undefined") {
      previewEl.textContent = markdown;
    }
  }

  // ---------------------------------------------------------------------------
  // 6. uploadFiles
  // ---------------------------------------------------------------------------
  function uploadFiles(files, textarea, uploadUrl) {
    if (!uploadUrl) return;

    Array.from(files).forEach(function (file) {
      const placeholder = "Uploading " + file.name + "...";
      insertAtCursor(textarea, placeholder);

      const formData = new FormData();
      formData.append("file", file);

      fetch(uploadUrl, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCSRFToken(),
        },
        body: formData,
      })
        .then(function (response) {
          if (!response.ok) throw new Error("Upload failed");
          return response.json();
        })
        .then(function (data) {
          const url = data.url || data.file_url || data.location || "";
          const name = data.name || file.name;
          const isImage = file.type.startsWith("image/");
          const replacement = isImage ? "![" + name + "](" + url + ")" : "[" + name + "](" + url + ")";
          replacePlaceholder(textarea, placeholder, replacement);
        })
        .catch(function () {
          replacePlaceholder(textarea, placeholder, "Upload failed: " + file.name);
        });
    });
  }

  function replacePlaceholder(textarea, placeholder, replacement) {
    const idx = textarea.value.indexOf(placeholder);
    if (idx === -1) return;
    textarea.value =
      textarea.value.substring(0, idx) +
      replacement +
      textarea.value.substring(idx + placeholder.length);
    triggerInput(textarea);
  }

  // ---------------------------------------------------------------------------
  // 7. getCSRFToken
  // ---------------------------------------------------------------------------
  function getCSRFToken() {
    // Try cookie
    const cookieMatch = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
    if (cookieMatch) return decodeURIComponent(cookieMatch[1]);

    // Try hidden input
    const input = document.querySelector("[name=csrfmiddlewaretoken]");
    if (input) return input.value;

    // Try meta tag
    const meta = document.querySelector("meta[name=csrf-token]");
    if (meta) return meta.getAttribute("content") || "";

    return "";
  }

  // ---------------------------------------------------------------------------
  // 8. initAll
  // ---------------------------------------------------------------------------
  function initAll() {
    document.querySelectorAll(".md-editor").forEach(initEditor);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAll);
  } else {
    initAll();
  }
})();
