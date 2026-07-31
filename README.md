# 📄 Smart PDF OCR Scanner & Sorter

## 📌 About the Project (Business Value)
This script was created to **automate and optimize repetitive office work**. The team had to manually review hundreds of non-searchable scanned PDFs looking for specific certificates and technical documents.

This project completely eliminates the human factor from this process. The script "reads" the images, finds the target keywords, automatically sorts the files, and generates an Excel report, **saving hours of manual work**.

## ⚙️ How it works

The script relies on OCR (Optical Character Recognition) technology.

1. **PDF to Image Conversion:** Uses `pypdfium2` to render low-quality PDF pages into images (with resolution scaling).
2. **Text Extraction (OCR):** Feeds the images into the `EasyOCR` engine to extract text (supports English and Polish).
3. **Analysis & Sorting:** The algorithm searches the extracted text for predefined keywords. If a match is found, it physically copies the file to the output folder (`shutil`).
4. **Reporting:** Finally, it creates an Excel report (`pandas`), making further verification easier for the team.

## 🛠️ Technologies Used

- **Python 3**
- **EasyOCR** (text detection and extraction from images)
- **PyPDFium2** (fast rendering of scanned PDFs)
- **Pandas / NumPy** (results aggregation and spreadsheet export)

## 🚀 How to run it locally

1. Install required libraries:
   ```bash
   pip install -r requirements.txt
