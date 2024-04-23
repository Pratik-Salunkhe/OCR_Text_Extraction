# main.py

import os
from ch_ocr_full import * #rename_pdfs, process_pdfs_in_folder, crop_pdf_dynamically, convert_pdf_to_images, perform_ocr


# Call rename_pdfs dynamically
#input_folder_path_rename = "/home/pratiksalunkhe/Vallabh/Fin_OCR_Model/pdf_input/"
#backup_folder_path_rename = "/home/pratiksalunkhe/Vallabh/Fin_OCR_Model/Name_backup_folder"
#rename_pdfs(input_folder_path_rename, backup_folder_path_rename)
# Call process_pdfs_in_folder dynamically
input_folder_path_extract = "/home/pratiksalunkhe/Vallabh/Fin_OCR_Model/pdf_input/"
output_directory_extract = "/home/pratiksalunkhe/Vallabh/Fin_OCR_Model/page_seperated_pdf"
process_pdfs_in_folder(input_folder_path_extract, output_directory_extract)
# Call crop_pdf_dynamically 
input_pdf_folder_crop = "/home/pratiksalunkhe/Vallabh/Fin_OCR_Model/page_seperated_pdf/"
for fol in os.listdir(input_pdf_folder_crop):
    fol_path = os.path.join(input_pdf_folder_crop, fol)
    for fold in os.listdir(fol_path):
        fold_path = os.path.join(fol_path, fold)
        for file in os.listdir(fold_path):
            if file.endswith(".pdf"):
                input_pdf_file = os.path.join(fold_path, file)
                for col_num in [0,-1]:
                    column_to_crop = col_num  # You can change this value dynamically
                    crop_pdf_dynamically(input_pdf_file, column_to_crop)
# Call convert_pdf_to_images 
input_pdf_to_img = "/home/pratiksalunkhe/Vallabh/Fin_OCR_Model/page_seperated_pdf/"
for fol in os.listdir(input_pdf_to_img):
    fol_path = os.path.join(input_pdf_to_img, fol)
    for fold in os.listdir(fol_path):
        fold_path = os.path.join(fol_path, fold)
        for pg_fol in os.listdir(fold_path):
            pg_fol_path = os.path.join(fold_path, pg_fol)
            if os.path.isdir(pg_fol_path):
                for crop_pdf_files in os.listdir(pg_fol_path):
                    ip_crop_pdf_files = os.path.join(pg_fol_path, crop_pdf_files)
                    convert_pdf_to_images(ip_crop_pdf_files)
# Call perform_ocr 
input_img_for_ocr = "/home/pratiksalunkhe/Vallabh/Fin_OCR_Model/pdf_to_img/"
for fol in os.listdir(input_img_for_ocr):
    fol_path = os.path.join(input_img_for_ocr, fol)
    for fold in os.listdir(fol_path):
        fold_path = os.path.join(fol_path, fold)
        for im_path in os.listdir(fold_path):
            pg_img_path = os.path.join(fold_path, im_path)
            if os.path.splitext(pg_img_path)[1] == '.jpg':
                perform_ocr(pg_img_path)
