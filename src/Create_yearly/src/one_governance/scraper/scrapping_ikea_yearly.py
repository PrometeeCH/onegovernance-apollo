import csv

import requests
from bs4 import BeautifulSoup


def scrape_and_save(url_: list, class_scrapp: str, output_file: str) -> None:
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["url", "contenue"])  # Write header

        for url in url_:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            elements = soup.find_all(class_=class_scrapp)
            for element in elements:
                writer.writerow([url, element.get_text().strip()])  # Write data
