import sys
import requests
import os
import re
import easyocr


class FastImageExtractor:
    def __init__(self):
        self.download_path = "downloaded_image.png"
        self.reader = easyocr.Reader(['en'], gpu=False)

    def download_from_link(self, link):
        """Download image from Google Drive link or direct URL"""
        try:
            if "drive.google.com" in link:
                if "/file/d/" in link:
                    file_id = link.split("/file/d/")[1].split("/")[0]
                elif "id=" in link:
                    file_id = link.split("id=")[1].split("&")[0]
                else:
                    raise ValueError("Invalid Google Drive link format")
                download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
            else:
                download_url = link

            print(f"📥 Downloading from: {download_url}")
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(download_url, headers=headers, timeout=15)
            response.raise_for_status()

            with open(self.download_path, 'wb') as f:
                f.write(response.content)

            print(f"✅ Image saved as: {self.download_path}")
            return self.download_path
        except Exception as e:
            raise Exception(f"Download failed: {str(e)}")

    def correct_characters(self, text):
        """Fix common OCR misclassifications"""
        corrections = {
            '5': '5',
            'S': '5',
            'Z': '7',
            '7': 'Z',
            '7': 'T',
            '7': 'Y',
            # 'Y': '7',
            '0': 'O',
            'O': '0'
        }
        fixed = ""
        for ch in text:
            if ch in corrections:
                fixed += corrections[ch]
            else:
                fixed += ch
        return fixed

    def extract_text(self, image_path):
        """Extract text using EasyOCR"""
        results = self.reader.readtext(image_path)

        best_text = ""
        best_prob = 0

        for (bbox, text, prob) in results:
            # cleaned = re.sub(r'[^A-Za-z0-9]', '', text)  # only alphanumeric
            cleaned = text.strip()
            cleaned = re.sub(r'[^A-Za-z0-9]', '', cleaned)
            cleaned = self.correct_characters(cleaned)   # apply correction
            if len(cleaned) >= 4 and prob > best_prob:
                best_text = cleaned
                best_prob = prob
            print(
                f"Detected: '{text}' → Cleaned: '{cleaned}' (confidence: {prob:.2f})")

            # if best_prob < 0.75:   # only if OCR not very confident
            #     best_text = self.correct_characters(best_text)

        # if best_prob < 0.75 and best_text:
        #     corrected = self.correct_characters(best_text)
        #     print(
        #         f"Low confidence → Applying correction: {best_text} → {corrected}")
        #     best_text = corrected

        return best_text, best_prob

    def process(self, input_path):
        """Main processing"""
        try:
            if input_path.startswith(('http://', 'https://')):
                image_path = self.download_from_link(input_path)
            else:
                image_path = input_path
                if not os.path.exists(image_path):
                    raise FileNotFoundError(f"File not found: {image_path}")

            print("🔍 Extracting text...")
            text, prob = self.extract_text(image_path)

            print("\n" + "="*50)
            print("📝 EXTRACTION RESULT:")
            print("="*50)
            if text:
                print(f"🎯 Best Text: '{text}' (confidence: {prob:.2f})")
            else:
                print("❌ No text detected!")
            return text
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return ""


def main():
    if len(sys.argv) != 2:
        print("Usage: python capture.py <image_path_or_link>")
        print("Examples:")
        print("  python capture.py image.png")
        print("  python capture.py https://drive.google.com/file/d/FILE_ID/view")
        return

    extractor = FastImageExtractor()
    result = extractor.process(sys.argv[1])

    if result:
        print(f"\n✅ Success! Extracted: {result}")


if __name__ == "__main__":
    main()
