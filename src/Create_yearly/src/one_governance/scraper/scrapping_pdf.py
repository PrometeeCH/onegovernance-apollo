import csv
import os

import requests
from langchain_community.document_loaders import PyPDFLoader


def extract_text_from_url_pdf(pdf_path: str, url: str, csv_output_path: str) -> None:
    if not os.path.exists(pdf_path):
        response = requests.get(url, timeout=10)
        # Enregistrer le fichier PDF
        with open(pdf_path, "wb") as f:
            f.write(response.content)

    # Charger le fichier PDF
    loader = PyPDFLoader(pdf_path)
    # loader = PdfReader(pdf_path)
    pages = loader.load_and_split()

    # Open the CSV file in write mode
    with open(csv_output_path, "w", newline="") as file:
        writer = csv.writer(file)

        # Write each page to a separate row in the CSV file
        writer.writerow(["page", "contenu"])
        for page in pages:
            writer.writerow([page.metadata["page"], page.page_content])


# Télécharger le fichier PDF
