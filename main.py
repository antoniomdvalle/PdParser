import fitz
import pandas as pd
import customtkinter as ctk
from tkinter import filedialog
import os
import re


# theme and appearance
ctk.set_default_color_theme("dark-blue") # blue, green, dark-blue
ctk.set_appearance_mode("system") # dark, light, system

class PdParser(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x450")
        self.title("PdParser")

        self.iconbitmap("assets/icon.ico")

        # 1. File browsing
        file_path = ""
        self.btn_browse = ctk.CTkButton(self, text="Select the PDF file", command=self.choose_file)
        self.btn_browse.pack(pady=20)

        # 2. Checking file browsing
        self.lbl_file_status = ctk.CTkLabel(self, text="No file selected", text_color="gray")
        self.lbl_file_status.pack(pady=10)

        # 3. Page number input
        self.label_page=ctk.CTkLabel(self, text="Enter page number:")
        self.label_page.pack(pady=10)

        self.page_entry=ctk.CTkEntry(self, placeholder_text="ex. 50")
        self.page_entry.pack(pady=5)

        # 4. Run button
        self.btn_run = ctk.CTkButton(self, text="Extract components", command=self.run_parser)
        self.btn_run.pack(pady=10)



    def choose_file(self):
            file_path = filedialog.askopenfilename(
                title="Select your PDF diagram",
                filetypes=[("PDF Files", "*.pdf")]
            )

            if file_path:
                self.selected_file_path = file_path
                #os.path.basename = "file.pdf" instead of C:/user/...
                file_name = os.path.basename(file_path)
                self.lbl_file_status.configure(text=f"Selected: {file_name}", text_color="white")
                print(f"File loaded: {file_path}")
    
    def run_parser(self):
        # SAFETY CHECKS
        if not self.selected_file_path:
            self.lbl_file_status.configure(text="ERROR: Please select a file first.", text_color="red")
            return

        pdf = fitz.open(self.selected_file_path)

        # page numeration
        page_num = self.page_entry.get()
        page_idx = int(page_num) - 1
        
        if not page_num.isdigit():
            self.lbl_file_status.configure(text="ERROR: Please type a valid page number!", text_color="red")
            return
        
        if page_idx < 1 or page_idx > len(pdf):
            self.lbl_file_status.configure(text=f"ERROR: Page {int(page_num)} is out of range.", text_color="red")
            return []



        print(f"Parsing file {self.selected_file_path} on page {page_num}...")

        
        # ___________________________ PARSING LOGIC ___________________________
        
        text = ""
        
        page_text = pdf[page_idx]

        text = page_text.get_text()

        pattern = r'\b\d*[A-Z]{1,4}\d*\b'

        components = re.findall(pattern, text)

        print(f"Components found on page {page_idx}: {len(text)}")

        df = pd.DataFrame(components, columns=['Components'])

        # WHITELIST
        valid_prefixes = ('K', 'Q', 'M', 'F', 'X', '1CX', '2CX', 'S', 'L', 'CLP', 'PLC', 'IHM', 'HMI', 'TX', 'B', 'G', 'ED', 'EA')
        df = df[df['Components'].str.startswith(valid_prefixes, na=False)]

        #BLACKLIST
        invalid_terms = [
            # --- SINGLE LETTERS / SHORT NOISE ---
            # Grid layout coordinates, single zones, or stray letters
            'B', 'F', 'M', 'S',

            # --- DIMENSIONS & GEOMETRY ---
            # Measurements, physical scales, and sheet sizes
            'A2', 'A3', 'A4', 'ESCALA', 'FORMATO', 'GRAU', 'KM', 'LxA', 'MM',

            # --- CORPORATE & REGISTERED ACRONYMS ---
            # Legal structures, corporate IDs, and professional registries
            'CEP', 'CNPJ', 'CREA', 'IE', 'INC', 'LTDA',

            # --- BRAZILIAN STATES ---
            # Address data from title blocks or manufacturer registries
            'BA', 'BR', 'CE', 'GO', 'MG', 'PE', 'PR', 'RJ', 'RS', 'SC', 'SP',

            # --- LOCATION & ADDRESS TERMS ---
            # Map navigation data from layout corners
            'AV', 'AVENIDA', 'BAIRRO', 'CIDADE', 'LOGRADOURO', 'MUNICIPIO', 
            'NRO', 'NUM', 'RUA', 'BRASIL',

            # --- PROJECT METADATA & CONTROL ---
            # Standard schematic frame data fields
            'APROV', 'APROVADO', 'CLIENTE', 'DATA', 'DESC', 'DESCRICAO', 
            'DESENHADO', 'DESENHO', 'EMISSAO', 'NOME', 'PROJETO', 'TITULO', 
            'VISTO',

            # --- ELECTRICAL SPECIFICATIONS & HARDWARE MATERIALS ---
            # Text descriptors next to physical components
            'ALUM', 'CABO', 'CHAVE', 'COBRE', 'DISJ', 'FIOS', 'PVC', 'TERM',

            # --- REVISIONS & NOTES ---
            # Review fields and side annotations
            'CONF', 'CONFORME', 'ITEM', 'NOTA', 'NOTAS', 'OBS', 'SEQ', 'SET', 
            'VEJA', 'VER',

            # --- PORTUGUESE STOPWORDS ---
            # Grammar elements caught from structural strings
            'COM', 'DAS', 'DOS', 'EMA', 'ETA', 'PARA', 'PELO', 'PELOS', 'POR', 
            'SEM', 'SER', 'SEUS', 'SOB', 'SOBRE', 'SUA', 'SUAS', 'UM', 'UMA'
        ]
        df = df[~df['Components'].isin(invalid_terms)]


        print(f"Valid components: {len(df)}")

        df.sort_values(by='Components', inplace=True) # se quiser de Z-A, bota inplace=False
        df.to_excel("components.xlsx", index=False, header=False)

        print("Converted sucessfully.")

if __name__ == "__main__":
    app = PdParser()
    app.mainloop()