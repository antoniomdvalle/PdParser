import pandas as pd
from watcher import search_components
import fitz


def convert():
    pdf = fitz.open("file.pdf")
    print(f"File opened. Total pages: {len(pdf)}.")

    target_page = input("Type your page:")

    converted_tgt_pg = int(target_page)

    if converted_tgt_pg < 1 or converted_tgt_pg > len(pdf):
        print(f"Error: Page {converted_tgt_pg} out of range.")
        return []

    components = search_components(converted_tgt_pg) #CHAMA O WATCHER

    print("Components found")

    df = pd.DataFrame(components, columns=['Components'])

    valid_prefixes = ('K', 'Q', 'M', 'F', 'X', '1CX', '2CX', 'S', 'L')

    df = df[df['Components'].str.startswith(valid_prefixes, na=False)]

    df.sort_values(by='Components', inplace=True) #se quiser de Z-A, ascending=False. O padrão já é True
    df.to_excel("components.xlsx", index=False, header=False)
