 
from chocr_text import *
import os

pdf_fold_path = "/home/pratiksalunkhe/Vallabh/Fin_OCR_Model/pdf_input"
for pdf in os.listdir(pdf_fold_path):
    pdf_path = os.path.join(pdf_fold_path,pdf)


    page_paths = extract_pages_and_save(pdf_path)
        # Example usage of crop_pdf_dynamically function
    crop_pdf_files = []
    for input_pdf_path in page_paths:
        crop_pdf_path = crop_pdf(input_pdf_path, crop_pdf_files)
    # Example usage seperating the Pdf Paths for first Column and Last column Pdfs
    col_0_pdf_path, col_1_pdf_path = filter_paths(crop_pdf_path)
    #print("Path for column_0 (Last_column)","\n",col_0_pdf_path)
    #print("Path for column_1 (first_column)","\n",col_1_pdf_path)
    # Example usage of convert_pdf_to_images function
    saved_image_paths = []
    for path in crop_pdf_files:
        saved_img = convert_pdf_to_images(path,saved_image_paths)
    # Example usage seperating the Image Paths for first Column and Last column images
    col_0_image_path, col_1_image_path = filter_paths(saved_img)
    #print("Path for column_0 (Last_column)","\n",col_0_image_path)
    #print("Path for column_1 (first_column)","\n",col_1_image_path)
    # Example usage of perform_ocr function
    for img_path in col_0_image_path:
        out_path = perform_ocr(img_path)
    for pdfs in col_1_pdf_path:
        pdf_path = pdfs
        output_file_path = extract_word_coordinates_from_pdf(pdf_path,out_path)
    print("Text extracted and saved to:", output_file_path)
    print("file sussefully prcessed >> ",pdfs)


