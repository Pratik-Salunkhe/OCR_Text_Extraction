# file2.py

from chocr_text import * # extract_pages_and_save, crop_pdf_dynamically, convert_pdf_to_images, perform_ocr
import os

directory_path = "/home/pratiksalunkhe/Vallabh/Fin_OCR_Model/pdf_input"
for pdf in os.listdir(directory_path):
    try:
        pdf_path = os.path.join(directory_path,pdf)
        text_extraction(pdf_path)
    except Exception as e:
        print(pdf_path)
# Example usage of extract_pages_and_save function
#pdf_path = "/home/pratiksalunkhe/Vallabh/Fin_OCR_Model/pdf_input/016.pdf"
#text_extraction(pdf_path)
#

    