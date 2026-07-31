import os
import shutil
import easyocr
import pypdfium2 as pdfium
import numpy as np
import pandas as pd
import openpyxl

# Path configuration - using relative paths
INPUT_FOLDER = "./input_pdfs"       # Folder containing scanned PDFs for analysis
OUTPUT_FOLDER = "./output_pdfs"     # Destination folder for matched documents
KEYWORDS = ["keyword_1", "keyword_2"]       # Keywords to search for

# Create directories if they do not exist
os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

print("Loading OCR engine (this will take a few seconds)...")

# Initialize the reader with Polish and English support
reader = easyocr.Reader(['pl', 'en'], gpu=False)

# Get all PDF files in the input folder
pdf_files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(".pdf")]
total_files = len(pdf_files)

print(f"Found {total_files} PDF files. Starting the process!\n")

results = []

for i, filename in enumerate(pdf_files, 1):
    file_path = os.path.join(INPUT_FOLDER, filename)
    print(f"[{i}/{total_files}] Analyzing file: {filename}...")
    
    try:
        pdf = pdfium.PdfDocument(file_path)
        full_text = ""
        
        # Iterate through all pages in the PDF
        for page in pdf:
            
            # Render page to an image. If quality is too low, scale can be increased to 3 or 4
            image_pil = page.render(scale=2).to_pil() 
            image_np = np.array(image_pil)
            
            # Extract text from the image
            text_list = reader.readtext(image_np, detail=0)
            full_text += " ".join(text_list).lower() + " "
        
        print(f"      [AI VISION]: {full_text[:300]}...")
        
        # Check if any of the keywords are present in the extracted text
        found = any(keyword in full_text for keyword in KEYWORDS)
        
        if found:
            print(f"   -> [MATCH FOUND!] Copying file to '{OUTPUT_FOLDER}'.")
            shutil.copy(file_path, os.path.join(OUTPUT_FOLDER, filename))
            
            results.append({
                "File Name": filename,
                "Status": "For manual review"
            })
                
    except Exception as e:
        print(f"   [ERROR] Failed to process file {filename}. Error: {e}")

# Generate Excel report if any files were matched
if results:
    df = pd.DataFrame(results)
    df.to_excel("ocr_results.xlsx", index=False) 
    print(f"\n✅ Done! Found and copied {len(results)} documents.")
    
else:
    print("\n❌ Process finished. No documents found matching the keywords.")