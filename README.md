🖼️ Fast Image Text Extractor

A Python tool that extracts text from images using EasyOCR.
Supports both local image files and Google Drive links, with built-in correction for common OCR misclassifications.

✨ Features

EasyOCR Integration – No Tesseract installation required

Google Drive Support – Extract text directly from shared Drive links

Local File Support – Process images from your filesystem

Character Correction – Fixes common OCR mistakes (e.g., confusing O with 0, S with 5)

Confidence Scoring – Shows probability for detected text

Simple CLI – Run with one command

🛠️ Installation

Clone this repo

git clone https://github.com/yourusername/fast-image-extractor.git
cd fast-image-extractor


Create virtual environment (optional but recommended)

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows


Install dependencies

pip install -r requirements.txt


✅ Unlike Tesseract-based tools, this project only needs EasyOCR + PyTorch (handled automatically).

🚀 Usage
Run from command line:
python capture.py <image_path_or_link>

Examples:

Local image

python capture.py ./captcha.png


Google Drive link

python capture.py "https://drive.google.com/file/d/FILE_ID/view"

📊 Example Output
📥 Downloading from: https://drive.google.com/uc?export=download&id=FILE_ID
✅ Image saved as: downloaded_image.png
🔍 Extracting text...
Detected: 'T4YnNi' → Cleaned: '747nNi' (confidence: 0.92)

==================================================
📝 EXTRACTION RESULT:
==================================================
🎯 Best Text: '747nNi' (confidence: 0.92)

🔧 How It Works

Input Handling – Accepts Drive links or local paths

Image Downloading – Downloads Drive images automatically

OCR – Uses EasyOCR (Reader(['en'])) to extract text

Cleaning – Removes non-alphanumeric characters

Correction – Applies mapping to fix OCR confusions (0 ↔ O, 5 ↔ S, 7 ↔ Z, etc.)

Result Selection – Chooses best match based on confidence

📁 Project Structure
fast-image-extractor/
├── capture.py           # Main application
├── requirements.txt     # Dependencies (EasyOCR, requests, etc.)
├── README.md            # Documentation

🐛 Troubleshooting

"torch not found" → Run pip install torch

"File not found" → Check your image path
