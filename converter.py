import pandas as pd
from watcher import search_components


components = search_components()
print("Components found")

def convert():
    df = pd.DataFrame(components)

    df.to_excel("components.xlsx", index=False, header=False)