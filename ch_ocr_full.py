
import os
import pandas as pd
import shutil
import PyPDF2
import camelot
from PyPDF2 import PdfFileReader, PdfFileWriter
from pdf2image import convert_from_path

# To rename the pdf files and store the rename list with old list in .csv file

def rename_pdfs(input_folder, backup_folder):
    # Create a backup folder if it doesn't exist
    os.makedirs(backup_folder, exist_ok=True)

    # Initialize a counter for generating unique 3-digit numbers
    counter = 1

    # Initialize lists to store original and renamed filenames
    original_filenames = []
    renamed_filenames = []

    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
    
        # Original file name (with extension)
        original_filenames.append(filename)
        # Original file path
        original_path = os.path.join(input_folder, filename)
        # New file name (3-digit number with leading zeros)
        new_filename = f"{counter:03d}.pdf"
        # Renamed file path
        new_path = os.path.join(input_folder, new_filename)
        # Record the renaming
        renamed_filenames.append(new_filename)
        # Rename the file
        os.rename(original_path, new_path)
        # Increment counter for the next file
        counter += 1

    # Create a DataFrame to store the record
    df = pd.DataFrame({'Original Name': original_filenames, 'Renamed Name': renamed_filenames})

    # Save the record to an Excel file in the backup folder
    excel_file_path = os.path.join(backup_folder, "renaming_record.xlsx")
    df.to_excel(excel_file_path, index=False)










# Extracting pages from the pdf saving the pages seperatelly as .pdf

def extract_pages_and_save(pdf_path, output_directory):
    # Open the PDF file
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        total_pages = pdf_reader.numPages

        # Create a directory for the PDF file
        folder_name = os.path.splitext(os.path.basename(pdf_path))[0]
        folder_path = os.path.join(output_directory, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        # Extract each page and save it in a separate directory
        for page_num in range(total_pages):
            # Create a directory for the current page
            page_folder_name = f"{folder_name}_pg{page_num + 1}"
            page_folder_path = os.path.join(folder_path, page_folder_name)
            os.makedirs(page_folder_path, exist_ok=True)

            # Save the current page in the page-specific directory
            page = pdf_reader.getPage(page_num)
            output_pdf_path = os.path.join(page_folder_path, f"{folder_name}_pg{page_num + 1}.pdf")
            with open(output_pdf_path, 'wb') as output_file:
                pdf_writer = PyPDF2.PdfFileWriter()
                pdf_writer.addPage(page)
                pdf_writer.write(output_file)



def process_pdfs_in_folder(input_folder, output_directory):
    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        pdf_path = os.path.join(input_folder, filename)
        extract_pages_and_save(pdf_path, output_directory)













# Croping boxex from page.pdf files

def crop_pdf_dynamically(input_pdf_path,column_to_crop):
   

    # Read the PDF and extract cell coordinates
    table = camelot.read_pdf(input_pdf_path, encoding='utf-8')
    cell = table[0].cells

   

    # Iterate through the cells and get coordinates for the specified column
    for j, i in enumerate(cell[3:]):  # Assuming skipping first 3 cells
        x1 = i[column_to_crop].x1
        y1 = i[column_to_crop].y1
        x2 = i[column_to_crop].x2
        y2 = i[column_to_crop].y2
        
 
        parent_directory = os.path.dirname(input_pdf_path)
        name = parent_directory.split('/')[-1]
        
            # Define the output file name based on index
        output_file_name = f"column_{column_to_crop+1}_row_{j+1}_{name}_cropped.pdf"
        output_pdf_directory_name = f"cropped_{name}_pdf"
        
        # Create the output PDF directory if it doesn't exist
        output_pdf_path = os.path.join(os.path.dirname(input_pdf_path), output_pdf_directory_name)
        if not os.path.exists(output_pdf_path):
            os.makedirs(output_pdf_path)
        # Open the input PDF file
        with open(input_pdf_path, 'rb') as input_pdf_file:
            reader = PdfFileReader(input_pdf_file)
            writer = PdfFileWriter()
            # Iterate through each page of the PDF
            for page_number in range(reader.getNumPages()):
                page = reader.getPage(page_number)
                # Crop the page using coordinates
                page.mediaBox.lowerLeft = (x1, y1)
                page.mediaBox.upperRight = (x2, y2)
                # Add the cropped page to the new PDF
                writer.addPage(page)
            # Write the cropped PDF to the output file
            with open(os.path.join(output_pdf_path, output_file_name), 'wb') as output_pdf_file:
                writer.write(output_pdf_file)
    return input_pdf_path 













# Code to convert pdf to images

def convert_pdf_to_images(pdf_file_path):
    if pdf_file_path.endswith('.pdf'):

        pdf_name = os.path.splitext(os.path.basename(pdf_file_path))[0]  # Extract PDF name

        

        parent_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(pdf_file_path)))))
        output_folder = os.path.join(parent_directory, 'pdf_to_img')
        os.makedirs(output_folder, exist_ok=True)

        folder_prefix = pdf_file_path.split('/')[-4]  # 007
        op_sub_fol = os.path.join(output_folder, folder_prefix)
        os.makedirs(op_sub_fol, exist_ok=True)

        sub_fol_prefix = pdf_file_path.split('/')[-3]  # 007
        op_sub_fold = os.path.join(op_sub_fol, sub_fol_prefix)
        os.makedirs(op_sub_fold, exist_ok=True)

        images = convert_from_path(pdf_file_path, dpi=600)
        saved_image_paths = []

        for idx, image in enumerate(images):
            image_path = os.path.join(op_sub_fold, f"{pdf_name}.jpg") #f"{pdf_name}_{idx + 1}.jpg"
            image.save(image_path, "JPEG")
            saved_image_paths.append(image_path)
        
        return saved_image_paths
    









    

    # Passing Images to OCR 

def perform_ocr(img_path):

    img_name = os.path.splitext(os.path.basename(img_path))[0] #column_0_row_1_007_pg1_cropped
    parent_directory = os.path.dirname(os.path.dirname(os.path.dirname(img_path))) #/home/pratiksalunkhe/Vallabh/Fin_OCR_Model/pdf_to_img
    child_fol = img_path.split('/')[-3] # 007
    child_fold = img_path.split('/')[-2]
    output_path = os.path.join(parent_directory, child_fol, child_fold, f'{img_name}')
    command = f"tesseract {img_path} {output_path} -l Devanagari --psm 6"
    os.system(command)
