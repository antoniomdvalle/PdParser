import re
import fitz

def search_components():
    pdf = fitz.open("file.pdf")
    print("File opened")

    text = ""

    for page in pdf:
        text += page.get_text()

    pattern = r'\b[A-Z]{1,4}\d*\b' #optional numbers

    components = re.findall(pattern, text)

    print("Components found")

    return components
