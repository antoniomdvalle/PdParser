# PdParser

A simple browser-based tool for extracting electrical component and wire identifiers from PDF files.

## Features

* Extract component identifiers from PDF files
* Extract wire identifiers
* Process a specific page or a range of pages
* Filter results using whitelist and blacklist rules
* Sort extracted identifiers alphabetically/numerically
* Export results as `.CSV`
* Runs directly in the browser — no backend required

## Technologies

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

## Extraction Modes

### Components

Extracts matching identifiers from the selected PDF pages, filters them, and sorts the results.

### Wires

Extracts the identifiers, filters them, duplicates the results, and sorts them. This can be useful when each wire identifier needs to appear twice in the output.

## How to Use

1. Open `index.html` in a web browser.
2. Select a PDF file.
3. Choose the starting and ending pages.
4. Select an extraction mode.
5. Click **Process PDF**.
6. Review the extracted results.
7. Click **Download .CSV** to export them.


## Project Structure

```text
PdParser/
├── assets/
├── index.html
├── main.js
├── style.css
└── .gitignore
```

## Notes

PdParser processes the PDF directly in the browser using PDF.js. The extraction logic relies on patterns and predefined whitelist/blacklist rules, so it is mainly intended for PDFs containing structured electrical identifiers.

## License

No license has been specified yet.
