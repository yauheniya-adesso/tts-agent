import os
from PyPDF2 import PdfReader, PdfWriter

def split_pdf_to_pages(pdf_path, output_folder):
    # Ordner erstellen, falls nicht vorhanden
    os.makedirs(output_folder, exist_ok=True)

    # PDF laden
    reader = PdfReader(pdf_path)
    num_pages = len(reader.pages)
    print(f"Gesamtzahl Seiten: {num_pages}")

    # Jede Seite als separate PDF speichern
    for i in range(num_pages):
        writer = PdfWriter()
        writer.add_page(reader.pages[i])

        output_path = os.path.join(output_folder, f"page_{i+1}.pdf")
        with open(output_path, "wb") as output_pdf:
            writer.write(output_pdf)
        print(f"Seite {i+1} gespeichert als {output_path}")

if __name__ == "__main__":
    input_pdf = "./pdf/2025_Wang+.pdf" 
    output_dir = "pdf_pages"       
    split_pdf_to_pages(input_pdf, output_dir)
