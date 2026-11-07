# CBZ PDF Optimizer

Convert CBZ comic archives into optimized PDF files using **intelligent page stitching** for a smoother, more natural reading experience.

![Demo](assets/demo.gif)

---

## 📖 Overview

**CBZ PDF Optimizer** is a Python application that converts CBZ comic archives into high-quality PDF files while intelligently stitching smaller consecutive pages together.

Instead of creating one PDF page for every image, the application analyzes page dimensions during conversion and automatically stitches compatible pages into larger PDF pages. This significantly reduces unnecessary page turns while preserving the original reading order and image quality.

Whether your CBZ files come from a mobile comic reader, your personal comic collection, or another source, the generated PDF is optimized for comfortable reading on tablets, laptops, and PDF readers.

---

## ✨ Features

* 📚 Convert CBZ archives into PDF
* 🧩 Intelligent page stitching
* 📄 Preserve original reading order
* ⚡ Fast processing of large comic chapters
* 🖼️ High-quality PDF generation
* 📦 Lightweight and easy to use
* 💻 Works with standard CBZ archives

---

## 🎯 Why This Project?

Traditional CBZ-to-PDF converters simply place every image onto its own PDF page.

However, many comics contain numerous small images that create unnecessary page turns and interrupt the reading experience.

CBZ PDF Optimizer solves this problem by intelligently identifying smaller consecutive pages and stitching them together whenever appropriate, producing cleaner, more readable PDFs without changing the story flow.

---

## 🖼️ Example Workflow

### Input

A CBZ archive containing comic pages.

![Input](assets/input-cbz.png)

↓

### Processing

* Extract comic pages
* Analyze page dimensions
* Detect smaller consecutive pages
* Stitch compatible pages together
* Generate optimized PDF

↓

### Output

An optimized PDF with fewer page turns and a more natural reading experience.

![Output](assets/output-pdf.png)

---

## 🎬 Demo

The animation below demonstrates the complete conversion process.

![Demo](assets/demo.gif)

---

## 🛠️ Tech Stack

* Python
* Pillow (PIL)
* PyMuPDF *(replace with your actual PDF library if different)*
* zipfile

---

## 📂 Project Structure

```text
CBZ-PDF-Optimizer/
│
├── main.py              # Application entry point
├── stitcher.py          # Intelligent page stitching algorithm
├── requirements.txt     # Project dependencies
├── README.md
├── .gitignore
│
└── assets/
    ├── demo.gif
    ├── input-cbz.png
    ├── stitched-pages.png
    └── output-pdf.png
```

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/harshitkushwah/CBZ-PDF-Optimizer.git
cd CBZ-PDF-Optimizer
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

> Replace `main.py` with your actual entry file if it has a different name.

---

## ⚙️ How It Works

1. Open a CBZ archive.
2. Extract every comic page.
3. Analyze image dimensions.
4. Identify smaller consecutive pages.
5. Stitch compatible pages together.
6. Generate an optimized PDF while preserving the original reading order.

---

## 🔮 Future Improvements

* Batch conversion
* Drag-and-drop support
* Adjustable stitching threshold
* Progress tracking
* Metadata preservation
* Command-line interface
* Export quality settings

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

**Harshit Kushwah**

If this project helped you, consider giving it a ⭐ on GitHub.
