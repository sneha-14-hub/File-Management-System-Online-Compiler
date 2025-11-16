# File Management System & Online Compiler

**A web application that combines a secure file management system with an in-browser online compiler.**  
Upload, organize, preview and share code & documents — then compile and run code snippets (multiple languages) directly from your browser.

---

## 🔎 Overview

This project provides two main modules:

1. **File Management System (FMS)**  
   - Upload, download, delete, rename files and folders  
   - Folder hierarchy, file preview (text, images, PDFs), metadata (size, type, modified date)  
   - Role-based access (Owner / Editor / Viewer) and shareable links

2. **Online Compiler**  
   - Write, save and run code in the browser (supports multiple languages)  
   - Run code inside a secure sandbox / containerized runner (server-side)  
   - Save snippets to your file system, view compilation output, and download binaries or outputs

---

## ✨ Features

- User authentication (JWT / session-based)
- Folder & file operations: create, rename, move, delete, upload, download
- File preview for text, images, and PDFs
- Search and filtering by name, type, date
- Versioning (basic snapshot of recent saves) — optional
- Online editor with syntax highlighting and autosave
- Compile & run for languages: Python, C, C++, Java
- Resource limits per run (time, memory, file size)
- Activity logs & basic audit trail
- Responsive UI + REST API backend
- Optional: WebSocket for real-time compile output

---

## 🧭 Tech Stack (suggested)

- **Frontend:** React (Vite) / TypeScript, Monaco Editor or CodeMirror, Tailwind CSS
- **Backend:** python
- **Compilation / Runner:** Docker containers (one container per run) or a sandboxed worker
- **Storage:** MongoDB (metadata) + AWS S3 / local filesystem for files
- **Auth:** JWT + bcrypt / OAuth optional
- **DevOps:** Docker Compose for local dev, CI (GitHub Actions) for test/build

---



