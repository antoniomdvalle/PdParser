import re
import fitz

def search_components(target_page):
    pdf = fitz.open("file.pdf")
    text = ""
    page_idx = target_page - 1
    pages = pdf[page_idx]

    text = pages.get_text()

    pattern = r'\b\d*[A-Z]{1,4}\d*\b' #optional numbers

    components = re.findall(pattern, text)

    print(f"Components found on page {target_page}: {len(components)}")

    return components
