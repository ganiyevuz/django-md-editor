(function () {
  "use strict";

  // ---------------------------------------------------------------------------
  // 1. TOOLBAR_BUTTONS
  // ---------------------------------------------------------------------------
  const TOOLBAR_BUTTONS = {
    heading: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M3.75 2a.75.75 0 0 1 .75.75V7h7V2.75a.75.75 0 0 1 1.5 0v10.5a.75.75 0 0 1-1.5 0V8.5h-7v4.75a.75.75 0 0 1-1.5 0V2.75A.75.75 0 0 1 3.75 2Z"/></svg>', title: "Heading", action: "heading" },
    bold: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M4 2h4.5a3.501 3.501 0 0 1 2.852 5.53A3.499 3.499 0 0 1 9.5 14H4a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1Zm1 7v3h4.5a1.5 1.5 0 0 0 0-3Zm3.5-2a1.5 1.5 0 0 0 0-3H5v3Z"/></svg>', title: "Bold (Ctrl+B)", action: "bold" },
    italic: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M6 2.75A.75.75 0 0 1 6.75 2h6.5a.75.75 0 0 1 0 1.5h-2.505l-3.858 9H9.25a.75.75 0 0 1 0 1.5h-6.5a.75.75 0 0 1 0-1.5h2.505l3.858-9H6.75A.75.75 0 0 1 6 2.75Z"/></svg>', title: "Italic (Ctrl+I)", action: "italic" },
    strikethrough: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M7.581 3.25c-2.036 0-2.778 1.082-2.778 1.786 0 .055.002.107.006.157a.75.75 0 0 1-1.496.114 3.56 3.56 0 0 1-.01-.271c0-1.832 1.75-3.286 4.278-3.286 1.418 0 2.721.58 3.514 1.093a.75.75 0 0 1-.814 1.26c-.64-.414-1.662-.853-2.7-.853Zm3.474 4.25h1.195a.75.75 0 0 1 0 1.5H3.75a.75.75 0 0 1 0-1.5h4.411c-.278-.09-.547-.194-.795-.31-.869-.409-1.56-.983-1.965-1.69H7.94c.263.395.678.722 1.204.983.551.272 1.21.467 1.911.517ZM8.012 12.75c1.648 0 2.86-.725 2.86-1.652 0-.107-.016-.222-.048-.339a.75.75 0 0 1 1.452-.376c.058.224.096.46.096.715 0 2.012-2.163 3.152-4.36 3.152-1.39 0-2.728-.473-3.614-1.236a.75.75 0 0 1 .985-1.13c.606.527 1.593.866 2.629.866Z"/></svg>', title: "Strikethrough", action: "strikethrough" },
    quote: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M1.75 2.5h12.5a.75.75 0 0 1 0 1.5H1.75a.75.75 0 0 1 0-1.5Zm4 5h8.5a.75.75 0 0 1 0 1.5h-8.5a.75.75 0 0 1 0-1.5Zm0 5h8.5a.75.75 0 0 1 0 1.5h-8.5a.75.75 0 0 1 0-1.5ZM2.5 7.75v6a.75.75 0 0 1-1.5 0v-6a.75.75 0 0 1 1.5 0Z"/></svg>', title: "Quote (Ctrl+Shift+.)", action: "quote" },
    code: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="m11.28 3.22 4.25 4.25a.75.75 0 0 1 0 1.06l-4.25 4.25a.749.749 0 0 1-1.275-.326.749.749 0 0 1 .215-.734L13.94 8l-3.72-3.72a.749.749 0 0 1 .326-1.275.749.749 0 0 1 .734.215Zm-6.56 0a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042L2.06 8l3.72 3.72a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215L.47 8.53a.75.75 0 0 1 0-1.06Z"/></svg>', title: "Code (Ctrl+E)", action: "code" },
    link: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z"/></svg>', title: "Link (Ctrl+K)", action: "link" },
    image: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M16 13.25A1.75 1.75 0 0 1 14.25 15H1.75A1.75 1.75 0 0 1 0 13.25V2.75C0 1.784.784 1 1.75 1h12.5c.966 0 1.75.784 1.75 1.75ZM1.75 2.5a.25.25 0 0 0-.25.25v10.5c0 .138.112.25.25.25h.94l4.72-6.03a.75.75 0 0 1 1.18 0l4.72 6.03h.94a.25.25 0 0 0 .25-.25V2.75a.25.25 0 0 0-.25-.25ZM5.5 6a1.5 1.5 0 1 1-3.001-.001A1.5 1.5 0 0 1 5.5 6Z"/></svg>', title: "Image", action: "image" },
    "ordered-list": { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M5 3.25a.75.75 0 0 1 .75-.75h8.5a.75.75 0 0 1 0 1.5h-8.5A.75.75 0 0 1 5 3.25Zm0 5a.75.75 0 0 1 .75-.75h8.5a.75.75 0 0 1 0 1.5h-8.5A.75.75 0 0 1 5 8.25Zm0 5a.75.75 0 0 1 .75-.75h8.5a.75.75 0 0 1 0 1.5h-8.5a.75.75 0 0 1-.75-.75ZM.924 10.32a.5.5 0 0 1-.851-.076l-.025-.059a.5.5 0 0 1 .09-.47l1.5-1.836a.5.5 0 0 1 .362-.179h.168a.5.5 0 0 1 .5.5v4a.5.5 0 0 1-1 0v-2.957l-.744.907Zm-.009-7.378a.5.5 0 0 1 .5-.442h.166a.5.5 0 0 1 .5.5v4a.5.5 0 1 1-1 0V4.18l-.747.912a.5.5 0 0 1-.768-.64l1.35-1.51Z"/></svg>', title: "Ordered List (Ctrl+Shift+7)", action: "ordered-list" },
    "unordered-list": { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M5.75 2.5h8.5a.75.75 0 0 1 0 1.5h-8.5a.75.75 0 0 1 0-1.5Zm0 5h8.5a.75.75 0 0 1 0 1.5h-8.5a.75.75 0 0 1 0-1.5Zm0 5h8.5a.75.75 0 0 1 0 1.5h-8.5a.75.75 0 0 1 0-1.5ZM2 14a1 1 0 1 1 0-2 1 1 0 0 1 0 2Zm1-6a1 1 0 1 1-2 0 1 1 0 0 1 2 0ZM2 4a1 1 0 1 1 0-2 1 1 0 0 1 0 2Z"/></svg>', title: "Unordered List (Ctrl+Shift+8)", action: "unordered-list" },
    "task-list": { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M2.5 1.75v11.5c0 .138.112.25.25.25h3.17a.75.75 0 0 1 0 1.5H2.75A1.75 1.75 0 0 1 1 13.25V1.75C1 .784 1.784 0 2.75 0h8.5C12.216 0 13 .784 13 1.75v7.736a.75.75 0 0 1-1.5 0V1.75a.25.25 0 0 0-.25-.25h-8.5a.25.25 0 0 0-.25.25Zm10.97 6.97 2 2a.75.75 0 0 1 0 1.06l-4.25 4.25a.75.75 0 0 1-1.06 0l-2-2a.75.75 0 1 1 1.06-1.06l1.47 1.47 3.72-3.72a.75.75 0 0 1 1.06 0ZM4.75 4h4.5a.75.75 0 0 1 0 1.5h-4.5a.75.75 0 0 1 0-1.5ZM4 7.75A.75.75 0 0 1 4.75 7h2.5a.75.75 0 0 1 0 1.5h-2.5A.75.75 0 0 1 4 7.75Z"/></svg>', title: "Task List", action: "task-list" },
    "horizontal-rule": { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M0 7.75A.75.75 0 0 1 .75 7h14.5a.75.75 0 0 1 0 1.5H.75A.75.75 0 0 1 0 7.75Z"/></svg>', title: "Horizontal Rule", action: "horizontal-rule" },
    table: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M0 1.75C0 .784.784 0 1.75 0h12.5C15.216 0 16 .784 16 1.75v12.5A1.75 1.75 0 0 1 14.25 16H1.75A1.75 1.75 0 0 1 0 14.25ZM6.5 6.5v3h3v-3Zm3-1.5v-3h-3v3Zm1.5 1.5v3H14v-3Zm0-1.5V2h-3v3ZM6.5 11v3h3v-3Zm1.5-9.5v3H14v-3Zm-6 6h3v-3H2Zm0 1.5v3h3v-3Zm0-6v3h3V2Z"/></svg>', title: "Table", action: "table" },
    attach: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M12.212 3.02a1.753 1.753 0 0 0-2.478.003l-5.83 5.83a3.007 3.007 0 0 0-.88 2.127c0 .795.315 1.551.88 2.116a2.996 2.996 0 0 0 4.243 0l5.113-5.113a.75.75 0 0 1 1.06 1.06L9.207 14.16a4.506 4.506 0 0 1-6.364 0 4.496 4.496 0 0 1-1.318-3.187A4.506 4.506 0 0 1 2.843 7.79l5.83-5.83a3.003 3.003 0 0 1 4.243 0 3.005 3.005 0 0 1 0 4.243l-5.83 5.83a1.503 1.503 0 0 1-2.122 0 1.503 1.503 0 0 1 0-2.122l5.113-5.113a.75.75 0 0 1 1.06 1.06l-5.113 5.113a.003.003 0 0 0 0 .002.002.002 0 0 0 .002 0l5.83-5.83a1.503 1.503 0 0 0 0-2.123Z"/></svg>', title: "Attach File", action: "attach" },
    mention: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M4.75 7.5A3.25 3.25 0 0 1 8 4.25a3.25 3.25 0 0 1 3.25 3.25v.583c0 .478-.387.917-.917.917a.916.916 0 0 1-.916-.917V5.167a.75.75 0 0 0-1.5 0v.034A3.21 3.21 0 0 0 6.25 4.75a2.75 2.75 0 0 0 0 5.5c.843 0 1.595-.377 2.1-.975.385.52.97.892 1.65.975v.5A4.75 4.75 0 1 1 12.75 6v1.5c0 1.175-.775 2.167-1.867 2.417A3.24 3.24 0 0 1 8 12.25a3.25 3.25 0 0 1-3.25-3.25V7.5Zm1.5 0a1.75 1.75 0 1 0 3.5 0 1.75 1.75 0 0 0-3.5 0Z"/></svg>', title: "Mention", action: "mention" },
    ref: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M1 7.775V2.75C1 1.784 1.784 1 2.75 1h5.025c.464 0 .91.184 1.238.513l6.25 6.25a1.75 1.75 0 0 1 0 2.474l-5.026 5.026a1.75 1.75 0 0 1-2.474 0l-6.25-6.25A1.752 1.752 0 0 1 1 7.775Zm1.5 0c0 .066.026.13.073.177l6.25 6.25a.25.25 0 0 0 .354 0l5.025-5.025a.25.25 0 0 0 0-.354l-6.25-6.25a.25.25 0 0 0-.177-.073H2.75a.25.25 0 0 0-.25.25ZM6 5a1 1 0 1 1 0 2 1 1 0 0 1 0-2Z"/></svg>', title: "Reference", action: "ref" },
    undo: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M1.22 6.28a.749.749 0 0 1 0-1.06l3.5-3.5a.749.749 0 1 1 1.06 1.06L3.561 5h7.188a4.75 4.75 0 0 1 0 9.5H5.75a.75.75 0 0 1 0-1.5h4.999a3.25 3.25 0 0 0 0-6.5H3.561l2.22 2.22a.749.749 0 1 1-1.06 1.06Z"/></svg>', title: "Undo (Ctrl+Z)", action: "undo", align: "right" },
    redo: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M14.78 6.28a.749.749 0 0 0 0-1.06l-3.5-3.5a.749.749 0 1 0-1.06 1.06L12.439 5H5.25a4.75 4.75 0 0 0 0 9.5h4.999a.75.75 0 0 0 0-1.5H5.25a3.25 3.25 0 0 1 0-6.5h7.189l-2.22 2.22a.749.749 0 1 0 1.06 1.06Z"/></svg>', title: "Redo (Ctrl+Shift+Z)", action: "redo", align: "right" },
    fullscreen: { icon: '<svg viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M1.75 10a.75.75 0 0 1 .75.75v2.5c0 .138.112.25.25.25h2.5a.75.75 0 0 1 0 1.5h-2.5A1.75 1.75 0 0 1 1 13.25v-2.5a.75.75 0 0 1 .75-.75Zm12.5 0a.75.75 0 0 1 .75.75v2.5A1.75 1.75 0 0 1 13.25 15h-2.5a.75.75 0 0 1 0-1.5h2.5a.25.25 0 0 0 .25-.25v-2.5a.75.75 0 0 1 .75-.75ZM2.75 1h2.5a.75.75 0 0 1 0 1.5h-2.5a.25.25 0 0 0-.25.25v2.5a.75.75 0 0 1-1.5 0v-2.5C1 1.784 1.784 1 2.75 1Zm10.5 0A1.75 1.75 0 0 1 15 2.75v2.5a.75.75 0 0 1-1.5 0v-2.5a.25.25 0 0 0-.25-.25h-2.5a.75.75 0 0 1 0-1.5Z"/></svg>', title: "Fullscreen", action: "fullscreen", align: "right" },
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
      case "strikethrough":
        wrapSelection(textarea, "~~", "~~");
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
      case "image":
        insertImage(textarea);
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
      case "horizontal-rule":
        insertAtCursor(textarea, "\n---\n");
        break;
      case "table":
        insertAtCursor(textarea, "\n| Header | Header |\n| ------ | ------ |\n| Cell   | Cell   |\n");
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

  function insertImage(textarea) {
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const value = textarea.value;
    const selected = value.substring(start, end);

    if (selected) {
      // Selected text becomes alt text
      const inserted = "![" + selected + "](url)";
      textarea.value = value.substring(0, start) + inserted + value.substring(end);
      // Place cursor on "url"
      const urlStart = start + selected.length + 4;
      textarea.selectionStart = urlStart;
      textarea.selectionEnd = urlStart + 3;
    } else {
      const inserted = "![alt](url)";
      textarea.value = value.substring(0, start) + inserted + value.substring(end);
      // Select "alt"
      textarea.selectionStart = start + 2;
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
