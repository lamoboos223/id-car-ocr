import pytesseract
from PIL import Image
import re

def extract_fields(text):
    # Initialize variables
    name = None
    id_number = None
    expiry_date = None
    
    # Print raw text for debugging
    print("\nRaw extracted text:")
    print("-" * 50)
    print(text)
    print("-" * 50)
    
    # Process each line
    for line in text.split('\n'):
        line = line.strip()
        print(f"Processing line: '{line}'")  # Debug line
        
        # Look for name (assuming it's in capital letters)
        if re.search(r'^[A-Z\s]+$', line) and len(line) > 5:
            print(f"Found potential name: {line}")
            name = line
        
        # Look for ID number (assuming it's alphanumeric)
        id_match = re.search(r'\b[A-Z0-9]{6,}\b', line)
        if id_match:
            print(f"Found potential ID: {id_match.group()}")
            id_number = id_match.group()
        
        # Look for expiry date
        date_match = re.search(r'\b(\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4})\b', line)
        if date_match:
            print(f"Found potential date: {date_match.group()}")
            expiry_date = date_match.group()
    
    return name, id_number, expiry_date

def main():
    # Set the path to the Tesseract executable
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    try:
        # Load and process the image
        image = Image.open('./2.png')
        
        # Perform OCR
        extracted_text = pytesseract.image_to_string(image)
        
        # Parse the extracted text
        name, id_number, expiry_date = extract_fields(extracted_text)
        
        # Print the extracted information
        print("\nExtracted Information:")
        print(f'Name: {name}')
        print(f'ID Number: {id_number}')
        print(f'Expiry Date: {expiry_date}')
        
    except FileNotFoundError:
        print("Error: Image file not found. Please check the file path.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()