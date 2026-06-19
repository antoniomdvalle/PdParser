import fitz
import pandas as pd
import customtkinter as ctk
from tkinter import filedialog
import os
import re
import subprocess
from pathlib import Path

# theme and appearance
ctk.set_default_color_theme("dark-blue") # blue, green, dark-blue
ctk.set_appearance_mode("system") # dark, light, system


class PdParser(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x450")
        self.title("PdParser")
        self.iconbitmap("assets/icon.ico")

        self.lbl_title=ctk.CTkLabel(self, text="Welcome!")
        self.lbl_title.pack(pady=50)

        self.lbl_title=ctk.CTkLabel(self, text="Choose an action:")
        self.lbl_title.pack(pady=5)
        
        # 0. - SCREEN SWITCHING
        self.btn_acess_components=ctk.CTkButton(self, text="Extract components", command=self.open_components)
        self.btn_acess_components.pack(pady=15)

        self.btn_acess_wires=ctk.CTkButton(self, text="Extract wires", command=self.open_wires)
        self.btn_acess_wires.pack(pady=15)

    def open_components(self):
        next_window = ComponentPdParser()

        self.destroy()

        next_window.mainloop()

    def open_wires(self):
        next_window = WirePdParser()

        self.destroy()

        next_window.mainloop()


    


class ComponentPdParser(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x450")
        self.title("Component Extraction - PdParser")

        self.iconbitmap("assets/icon.ico")



        # 0. Main screen button
        self.btn_main_screen=ctk.CTkButton(self, text="Back to main screen", command=self.open_main_screen)
        self.btn_main_screen.pack(pady=15)
        
        # 1. File browsing
        file_path = ""
        self.btn_browse = ctk.CTkButton(self, text="Select the PDF file", command=self.choose_file)
        self.btn_browse.pack(pady=20)

        # 2. Checking file browsing
        self.lbl_file_status = ctk.CTkLabel(self, text="No file selected", text_color="gray")
        self.lbl_file_status.pack(pady=10)

        # 3. Check if the user wants all pages
        self.all_pages_var = ctk.IntVar(value=0)
        self.chk_all_pages = ctk.CTkCheckBox(self, text="Extract from all pages", variable=self.all_pages_var, command=self.checkbox_event)
        self.chk_all_pages.pack(pady=15)

        # 4. Page number input
        self.label_page_1=ctk.CTkLabel(self, text="Enter first (or only) page number:")
        self.label_page_1.pack(pady=10)

        self.page_entry_1=ctk.CTkEntry(self, placeholder_text="ex. 50")
        self.page_entry_1.pack(pady=5)


        # 5. Page number input
        self.label_page_2=ctk.CTkLabel(self, text="Enter the second page number (or leave 0 if unneeded):")
        self.label_page_2.pack(pady=10)

        self.page_entry_2=ctk.CTkEntry(self, placeholder_text="ex. 51")
        self.page_entry_2.pack(pady=5)

        # 6. Run button
        self.btn_run = ctk.CTkButton(self, text="Extract components", command=self.run_parser)
        self.btn_run.pack(pady=10)

        # 7. Confirmation label
        self.label_confirmation=ctk.CTkLabel(self, text="")
        self.label_confirmation.pack(pady=5)

    def checkbox_event(self):
        if self.all_pages_var.get() == 1:
            self.page_entry_1.delete(0, "end")
            self.page_entry_2.delete(0, "end")
            self.page_entry_1.configure(state="disabled", fg_color="#CBCBCB")
            self.page_entry_2.configure(state="disabled", fg_color="#CBCBCB")
        else:
            self.page_entry_1.configure(state="normal", fg_color=["#F9F9FA", "#343638"],placeholder_text="ex. 50")
            self.page_entry_2.configure(state="normal", fg_color=["#F9F9FA", "#343638"],placeholder_text="ex. 51")


    def open_main_screen(self):
        next_window = PdParser()

        self.destroy()

        next_window.mainloop()

    def search_components_from_text(self, text):
        pattern = r'\b\d*[A-Z]{1,4}\d*\b'
        return re.findall(pattern, text)

    def choose_file(self):
            file_path = filedialog.askopenfilename(
                title="Select your PDF diagram",
                filetypes=[("PDF Files", "*.pdf")]
            )

            if file_path:
                self.selected_file_path = file_path
                #os.path.basename = "file.pdf" instead of C:/user/...
                file_name = os.path.basename(file_path)
                self.lbl_file_status.configure(text=f"Selected: {file_name}", text_color="blue")
    
    def run_parser(self):
        # ___________________________ SAFETY CHECKS ___________________________
        if not self.selected_file_path:
            self.lbl_file_status.configure(text="ERROR: Please select a file first.", text_color="red")
            return


        # OPEN THE FILE
        pdf = fitz.open(self.selected_file_path)
        total_pages = len(pdf)
        all_found_components = []

        page_num_raw = self.page_entry_1.get()
        page_num_raw_2 = self.page_entry_2.get()

        # EXTRACT FROM ALL PAGES
        if self.all_pages_var.get() == 1:
            start_page = 1
            end_page = total_pages
#            for page in pdf:
#                text = page.get_text()
#                all_found_components.extend(self.search_components_from_text(text))

        else:

            start_raw = self.page_entry_1.get()
            end_raw = self.page_entry_2.get()


            if not start_raw.isdigit() or not end_raw.isdigit():
                self.lbl_file_status.configure(text="ERROR: Pages must be valid numbers")
                return


            start_page = int(start_raw)
            end_page = int(end_raw)

            if not page_num_raw.isdigit() or not page_num_raw_2.isdigit():
                self.lbl_file_status.configure(text="ERROR: Please type a valid page number!", text_color="red")
                return

            if page_num_raw_2 == 0:
                pass

            page_num = int(page_num_raw)
            page_num_2 = int(page_num_raw_2)

            if page_num < 1 or page_num > len(pdf):
                self.lbl_file_status.configure(text=f"ERROR: Page {int(page_num)} is out of range.", text_color="red")
                return []
            
            
            if page_num_2 < 1 or page_num_2 > len(pdf):
                self.lbl_file_status.configure(text=f"ERROR: Page {int(page_num_2)} is out of range.", text_color="red")
                return []


            
            text = pdf[page_num - 1].get_text()
            all_found_components = self.search_components_from_text(text)

        
        # ___________________________ PARSING LOGIC ___________________________

        #print(f"Components found on page {page_num}: {len(all_found_components)}")

        df = pd.DataFrame(all_found_components, columns=['Components'])

        # WHITELIST
        valid_prefixes = (
            '1','2','3','4','5','6','7','8','9','0','K', 'Q', 'M', 'F', 'X', '1CX', '2CX', 'S', 'L', 'CLP', 
            'PLC', 'IHM', 'HMI', 'TX', 'B', 'G', 'ED', 'EA','RL','RLS', 'F', 'IF', 'SW', 'FT'
        )
        df = df[df['Components'].str.startswith(valid_prefixes, na=False)]

        #BLACKLIST
        invalid_terms = [
            # --- SINGLE LETTERS / SHORT NOISE ---
            # Grid layout coordinates, single zones, or stray letters
            'B', 'F', 'M',

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

            # --- ELECTRICAL & HARDWARE MATERIALS ---
            # Text descriptors next to physical components
            'ALUM', 'CABO', 'CHAVE', 'COBRE', 'DISJ', 'FIOS', 'PVC', 'TERM', '16A',

            # --- REVISIONS & NOTES ---
            # Review fields and side annotations
            'CONF', 'CONFORME', 'ITEM', 'NOTA', 'NOTAS', 'OBS', 'SEQ', 'SET', 
            'VEJA', 'VER',

            # --- PORTUGUESE WORDS ---
            # Grammar elements caught from structural strings
            'COM', 'DAS', 'DOS', 'EMA', 'ETA', 'PARA', 'PELO', 'PELOS', 'POR', 
            'SEM', 'SER', 'SEUS', 'SOB', 'SOBRE', 'SUA', 'SUAS', 'UM', 'UMA'
        ]
        df = df[~df['Components'].isin(invalid_terms)]


        print(f"Valid components: {len(df)}")

        df.sort_values(by='Components', inplace=True) # se quiser de Z-A, bota inplace=False
        df.to_excel("components.xlsx", index=False, header=False)

        saida = Path("components.xlsx").resolve()

        print("Converted sucessfully.")

        subprocess.Popen(f'explorer /select,"{saida}"')

        self.label_confirmation.configure(text="Conversion ocurred sucessfully!")
        
class WirePdParser(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x450")
        self.title("Wire PdParser")
        
        self.iconbitmap("assets/icon.ico")



        # 0. Main screen button
        self.btn_main_screen=ctk.CTkButton(self, text="Back to main screen", command=self.open_main_screen)
        self.btn_main_screen.pack(pady=15)

        # 1. File browsing
        file_path = ""
        self.btn_browse = ctk.CTkButton(self, text="Select the PDF file", command=self.choose_file)
        self.btn_browse.pack(pady=20)

        # 2. Checking file browsing
        self.lbl_file_status = ctk.CTkLabel(self, text="No file selected", text_color="gray")
        self.lbl_file_status.pack(pady=10)



    def open_main_screen(self):
        next_window = PdParser()

        self.destroy()

        next_window.mainloop()
    
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
    

if __name__ == "__main__":
    app = PdParser()
    app.mainloop()