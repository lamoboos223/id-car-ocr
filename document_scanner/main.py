from paddleocr import PaddleOCR
import re

class DocumentScanner:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')
        
    def extract_info(self, image_path):
        # Read the image
        results = self.ocr.ocr(image_path, cls=True)
        
        # Initialize dictionary to store extracted information
        info = {
            'name': None,
            'date_of_birth': None,
            'id_number': None,
            'expiry_date': None
        }
        
        # Process each detected text
        for line in results:
            for word_info in line:
                text = word_info[1][0]  # Get the text
                confidence = word_info[1][1]  # Get the confidence score
                print(f"Detected text: {text} (confidence: {confidence:.2f})")  # Debug line
                
                # Same extraction logic as above
                if re.search(r'^[A-Z\s]+$', text) and len(text) > 5:
                    info['name'] = text
                
                dob_match = re.search(r'\d{2}[/-]\d{2}[/-]\d{4}|\d{2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}', text, re.IGNORECASE)
                if dob_match and not info['date_of_birth']:
                    info['date_of_birth'] = dob_match.group()
                
                id_match = re.search(r'[A-Z0-9]{6,}', text)
                if id_match and not info['id_number']:
                    info['id_number'] = id_match.group()
                    
        return info

def main():
    scanner = DocumentScanner()
    image_path = "./2.png"  # Update this path
    
    info = scanner.extract_info(image_path)
    
    print("\nExtracted Information:")
    for key, value in info.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
