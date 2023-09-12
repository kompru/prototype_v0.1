from PIL import Image, UnidentifiedImageError, ImageEnhance
import pytesseract
import requests
from io import BytesIO
import csv
import re
import tempfile
import time

pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

def download_image(url):
    print("Downloading image...")
    filename = None

    if "drive.google.com" in url:
        file_id = re.search(r'file/d/(.*?)/view', url)
        if file_id:
            file_id = file_id.group(1)
            url = f"https://drive.google.com/uc?export=download&id={file_id}"
            filename = file_id

    print(f"Attempting to download from URL: {url}")

    response = requests.get(url)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        temp_file.write(response.content)
        print(f"Saved downloaded content to temporary file {temp_file.name}")

    try:
        img = Image.open(BytesIO(response.content))

        # Enhance image before OCR
        # Define enhancement factors (adjust these as needed)
        # all go from 0.0 to 2.0, 1.0 is original image
        color_factor = 1.0  
        contrast_factor = 1.0  
        brightness_factor = 1.0
        sharpness_factor = 1.0 

        

        # Color Enhancement
        color_enhancer = ImageEnhance.Color(img)
        img = color_enhancer.enhance(color_factor)

        # Contrast Enhancement
        contrast_enhancer = ImageEnhance.Contrast(img)
        img = contrast_enhancer.enhance(contrast_factor)

        # Brightness Enhancement
        brightness_enhancer = ImageEnhance.Brightness(img)
        img = brightness_enhancer.enhance(brightness_factor)

        # Sharpness Enhancement
        sharpness_enhancer = ImageEnhance.Sharpness(img)
        img = sharpness_enhancer.enhance(sharpness_factor)

        # Save or further process the enhanced image
        img.save("enhanced_image.jpg")

        print("Image downloaded and enhanced.")
        return img, filename  # Return both image and filename
    except UnidentifiedImageError:
        print("Cannot identify image. Please make sure the URL points to a valid image file.")
        return None, None  # Return None for both image and filename

def ocr_image(image):
    #print("Performing OCR...")
    image = image.resize((image.width * 2, image.height * 2), resample=Image.LANCZOS)
    text = pytesseract.image_to_string(image)
    #print(f"Original OCR Output: {text}")  # Log original OCR output
    
    relevant_numbers = re.findall(r'\b\d{13}\b', text)
    
    if not relevant_numbers:  # Check if list is empty
        print("No 13-digit numbers found.")
    else:
        print(f"Total number of 13-digit numbers found: {len(relevant_numbers)}")  # Changed Line
    
    filtered_text = ' '.join(relevant_numbers)
    #print("OCR complete.")
    #print(f"Extracted numbers: {filtered_text}")
    return filtered_text

# ... (code after remains unchanged)


def save_to_csv(text, csv_filename='output.csv'):
    original_filename = csv_filename.split('.')[0]
    new_filename = f"{original_filename}_output.csv"

    print("Saving to CSV...")
    with open(new_filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        for line in text.split('\n'):
            csv_writer.writerow([str(cell) for cell in line.split()])
    print(f"Saved to {new_filename}")

# Dictionary to store contrast factor and corresponding 13-digit number count
contrast_results = {}  # Added Line

# User-configurable factors range, step, and whether to iterate
start_factor = 1.0
end_factor = 2.0
step_factor = 0.2

# Flags to control whether to iterate through each factor
iterate_contrast = True
iterate_color = False
iterate_brightness = False
iterate_sharpness = False

# A set to keep track of distinct 13-digit sequences found
distinct_13_digits = set()

if __name__ == "__main__":
    image_url = "https://drive.google.com/file/d/1APbrqxO-GS-BbDt3x3yBCm9K7p3z0X4k/view?usp=drive_link"
    original_image, filename = download_image(image_url)

    if original_image:
        start_time = time.time()
        factor_range = [round(x * step_factor, 1) for x in range(int(start_factor / step_factor), int(end_factor / step_factor) + 1)]
        
        contrast_range = factor_range if iterate_contrast else [1.0]
        color_range = factor_range if iterate_color else [1.0]
        brightness_range = factor_range if iterate_brightness else [1.0]
        sharpness_range = factor_range if iterate_sharpness else [1.0]

        # Initialize empty dictionary to store results
        results = {}

        for contrast_factor in contrast_range:
            for color_factor in color_range:
                for brightness_factor in brightness_range:
                    for sharpness_factor in sharpness_range:
                        image = original_image.copy()

                        print(f"Applying factors: C={color_factor}, Co={contrast_factor}, B={brightness_factor}, S={sharpness_factor}")

                        # Enhancements
                        image = ImageEnhance.Color(image).enhance(color_factor)
                        image = ImageEnhance.Contrast(image).enhance(contrast_factor)
                        image = ImageEnhance.Brightness(image).enhance(brightness_factor)
                        image = ImageEnhance.Sharpness(image).enhance(sharpness_factor)
                        
                        ocr_text = ocr_image(image)
                        found_sequences = re.findall(r'\b\d{13}\b', ocr_text)
                        count_13_digit = len(found_sequences)
                        
                        # Save distinct sequences
                        distinct_13_digits.update(found_sequences)
                        
                        key = f"C={color_factor}, Co={contrast_factor}, B={brightness_factor}, S={sharpness_factor}"
                        results[key] = count_13_digit
                        
                        # Commenting out the part that generates the .csv file
                        # if filename:
                        #     save_to_csv(ocr_text, csv_filename=f"{filename}_{key}")
                        # else:
                        #     save_to_csv(ocr_text, csv_filename=f"output_{key}")

        # Display Results at the end
        print("\nFinal Results:")
        for factors, count in results.items():
            print(f"- {factors} - 13-digit numbers found: {count}")

        # Display distinct sequences
        print(f"\nDistinct 13-digit sequences found: {len(distinct_13_digits)}")
        #print(f"Sequences: {', '.join(distinct_13_digits)}")
        end_time = time.time()
        print(f"Time taken: {end_time - start_time:.2f} seconds")

import pickle

# Save distinct_13_digits to a file
with open('distinct_13_digits.pkl', 'wb') as f:
    pickle.dump(distinct_13_digits, f)
