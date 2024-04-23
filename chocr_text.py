

import os
import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter
from pdf2image import convert_from_path
import camelot
import fitz




# ------------------ This function extracts each page from a PDF file and saves it as a separate PDF file in a structured directory. ------------------ #

"""
Open the PDF and determine the total number of pages
Create a directory to store extracted pages
For each page:
- Create a subdirectory for the page
- Save the page as a separate PDF in the subdirectory
- Append the path of the saved page to a list
Return the list of extracted PDF paths
"""


def extract_pages_and_save(pdf_path):
    # Open the PDF file
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        total_pages = pdf_reader.numPages

        # Create a directory for the PDF file
        folder_name = os.path.splitext(os.path.basename(pdf_path))[0]


        output_directory = os.path.join(os.path.dirname(os.path.dirname(pdf_path)), 'separate_pdf')

        folder_path = os.path.join(output_directory, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        # Extract each page and save it in a separate directory
        page_paths = []  # List to store paths of extracted pages
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
                
            # Append the path of the saved page to the list
            page_paths.append(output_pdf_path)
        
        return page_paths  # Return the list of extracted PDF paths



# ------------------ This function uses Camelot to  crop specified columns from a PDF based on cell coordinates ------------------ #

"""
Read the PDF and extract cell coordinates
For each specified column:
Calculate cell coordinates and define output file name
Create output directory if needed
Crop each page and save it to the output directory
Append the path of the cropped PDF to a list
Return the list of cropped PDF paths
"""

def crop_pdf(input_pdf_path, crop_pdf_files):
    # Read the PDF and extract cell coordinates
    table = camelot.read_pdf(input_pdf_path, encoding='utf-8')
    cell = table[0].cells
    for column_to_crop in [0,-1]:
        # Iterate through the cells and get coordinates for the specified column
        for index, element in enumerate(cell[3:]):  # Assuming skipping first 3 cells
            x1 = element[column_to_crop].x1
            y1 = element[column_to_crop].y1
            x2 = element[column_to_crop].x2
            y2 = element[column_to_crop].y2

            parent_directory = os.path.dirname(input_pdf_path)
            name = parent_directory.split('/')[-1]

            # Define the output file name based on index
            output_file_name = f"column_{column_to_crop+1}_row_{index+1}_{name}_cropped.pdf"
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
                    crop_pdf_files.append(os.path.join(output_pdf_path, output_file_name))
    return crop_pdf_files



# ------------------ Seperating list of paths as Col1(First_Column) and Col0(Last_Column) ------------------ #

def filter_paths(file_paths):
    column_0_paths = []
    column_1_paths = []
    for path in file_paths:
        if "column_0" in path:
            column_0_paths.append(path)
        else:
            column_1_paths.append(path)
    return column_0_paths, column_1_paths


# ------------------ This function converts a PDF file into images saving them with a JPG extension  ------------------ #
"""
Extract the PDF name and define the output folder path based on the file's parent directory and subfolders
Convert the PDF into images with a DPI of 600
Save each image in the output folder with the PDF name as the filename and a JPG extension.
Append the paths of the saved images to a list
Return the list of saved image paths
"""

def convert_pdf_to_images(pdf_file_path,saved_image_paths):
    if pdf_file_path.endswith('.pdf'):

        pdf_name = os.path.splitext(os.path.basename(pdf_file_path))[0]  # Extract PDF name


        pdf_name = os.path.splitext(os.path.basename(pdf_file_path))[0]  # Extract PDF name
        parent_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(pdf_file_path))))
        sub_fol1 = pdf_file_path.split('/')[-4]
        sub_fol2 = pdf_file_path.split('/')[-3]
        output_folder = os.path.join(parent_directory,sub_fol1,sub_fol2 ,'pdf_to_images')
        os.makedirs(output_folder, exist_ok=True)



        images = convert_from_path(pdf_file_path, dpi=600)
        

        for idx, image in enumerate(images):
            image_path = os.path.join(output_folder, f"{pdf_name}.jpg") #f"{pdf_name}_{idx + 1}.jpg"
            image.save(image_path, "JPEG")
            saved_image_paths.append(image_path)
        
        return saved_image_paths
    



 # ------------------ This function performs OCR using Tesseract on an image and returns the path where the OCR results are saved ------------------ #

"""
Extract the image name and relevant directory information from the path
Define the output path
Construct and execute the Tesseract command
Return the output path
"""

def perform_ocr(img_path):
    img_name = os.path.splitext(os.path.basename(img_path))[0] #column_0_row_1_007_pg1_cropped

    parent_directory = os.path.dirname(os.path.dirname(os.path.dirname(img_path))) #/home/pratiksalunkhe/Vallabh/Fin_OCR_Model/pdf_to_img

    child_fol = img_path.split('/')[-3] # 007

    child_fold = img_path.split('/')[-2]

    output_path = os.path.join(parent_directory, child_fol, child_fold, f'{img_name}')

    command = f"tesseract {img_path} {output_path} -l Devanagari --psm 6"

    os.system(command)

    return output_path




# ------------------ This function extracts word coordinates from a PDF file and saves them in a text file, using predefined directory structure for output   ------------------ #



def extract_word_coordinates_from_pdf(pdf_path,out_path):

    parent_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(pdf_path))))


    child_fol = pdf_path.split('/')[-4] # 007

    child_fold = pdf_path.split('/')[-3] # 007_pg3

    final_fold = os.path.join(parent_directory, child_fol, child_fold)
    if os.path.exists('pdf_to_images'):
        folder = 'pdf_to_images'

        output_folder = os.path.join(parent_directory, child_fol, child_fold,folder)

        doc = fitz.open(pdf_path)
        page = doc[0]
        word_coordinates_list = page.get_text("words", sort=True)
        doc.close()

        # Extract text from word coordinates list
        extracted_text = ' '.join([word[4] for word in word_coordinates_list])

        # Save extracted text to a text file
        file_name = os.path.splitext(os.path.basename(pdf_path))[0] + ".txt"
        file_path = os.path.join(output_folder, file_name)
        with open(file_path, 'w') as f:
            f.write(extracted_text)

    return file_path




# ------------------ This function calls all the above functions which is then called in chocr_main.py file   ------------------ #



def text_extraction(pdf_path):
  

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


    