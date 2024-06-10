import time
import csv
import re
import pandas as pd


from scraper.scrapping_ikea_project import IkeaScraper
from one_governance.scraper.scrapping_ikea_yearly import scrape_and_save
from one_governance.scraper.scrapping_pdf import extract_text_from_url_pdf

# arguments des parties a scrapper:
projet_ikea = False
yearly_report_ikea = False
pdf_template = True


### scrapping des projets ikea
if projet_ikea:
    print("Scrapping project ikea en cours...")
    start_time = time.time()

    scraper = IkeaScraper()
    scraper.fetch_links()
    scraper.scrape_all_projects()
    scraper.save_to_csv()

    end_time = time.time()
    execution_time = end_time - start_time
    print(
        f"Le temps d'exécution du scrapping des projets du site ikea est de {execution_time:.2f} secondes."
    )

### scrapping des données pour le yearly report ikea
if yearly_report_ikea:
    print("Scrapping yearly ikea en cours...")

    start_time = time.time()

    # page du site a scrapper pour le yearly report
    url_scrapp = [
        "https://ikeafoundation.org/about/",
        "https://ikeafoundation.org/values/",
        "https://ikeafoundation.org/the-way-we-work/",
        "https://ikeafoundation.org/themes/",
    ]
    class_scrapp = "entry__inner padded container has-parent-"
    output_file = "../../data/yearly_report_data.csv"

    scrape_and_save(url_scrapp, class_scrapp, output_file)

    # pdf a scrapper pour le yearly report
    url_pdf = (
        "https://ikeafoundation.org/wp-content/uploads/2023/07/Annual-Review-2022.pdf"
    )
    pdf_path = "../../data/Annual-Review-2022.pdf"
    output_file = "../../data/annualrewiew2022.csv"
    extract_text_from_url_pdf(pdf_path, url_pdf, output_file)

    end_time = time.time()
    execution_time = end_time - start_time
    print(
        f"Le temps d'exécution du scrapping du pdf et des page pour yearly du site ikea est de {execution_time:.2f} secondes."
    )
if pdf_template:
    url_pdf = ""
    pdf_path = "../../data/Annual-Review-template.pdf"
    output_file = "../../data/annualrewiew_template.csv"
    extract_text_from_url_pdf(pdf_path, url_pdf, output_file)
    # Lecture du fichier csv dans un dataframe pandas
    df = pd.read_csv(output_file)
    col_str = ' '.join(df['contenu'])

        # Préparation d'une liste pour stocker les résultats
    result = []

    parts = re.split(r'(\d+)\.\s*', col_str)
    for i in range(1, len(parts), 2):
        # Ajout de chaque partie à la liste
        result.append({'partie': parts[i], 'contenu': parts[i+1].strip()})

    # Conversion de la liste en un DataFrame puis enregistrement dans un nouveau fichier csv
    result = pd.DataFrame(result)
    result.to_csv(output_file, index=False)
