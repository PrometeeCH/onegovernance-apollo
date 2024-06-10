import os

import pandas as pd
import requests
from bs4 import BeautifulSoup


class IkeaScraper:
    def __init__(self) -> None:
        self.base_url = "https://ikeafoundation.org/grants/page/"
        self.links: list[str] = []
        self.data: list[dict] = []

    def fetch_links(self, num_pages: int = 53) -> None:
        for page_num in range(1, num_pages + 1):
            url = f"{self.base_url}{page_num}/"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                articles = soup.select("article > a")
                for article in articles:
                    link = article.get("href")
                    if link:
                        self.links.append(link)
            else:
                print(f"Failed to retrieve page {page_num}")

    def scrape_project(self, url: str) -> None:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.find(class_="entry__title border-header h2")
            description = soup.find(class_="grants-hero__description h4")
            total_granted = soup.find(class_="grant-payout__total")
            total_paid = soup.find(class_="grant-payout__paid")
            grant_results = soup.find_all(class_="grant-payout__result")
            partner = soup.find(class_="partner-single-card__title h5")

            # Extract text or default to 'N/A'
            project_data = {
                "URL": url,
                "Title": title.get_text(strip=True) if title else "N/A",
                "Description": description.get_text(strip=True)
                if description
                else "N/A",
                "Total Granted": total_granted.get_text(strip=True)
                if total_granted
                else "N/A",
                "Total Paid": total_paid.get_text(strip=True) if total_paid else "N/A",
                "Date Granted": grant_results[0].get_text(strip=True)
                if grant_results
                else "N/A",
                "Geographic Area": grant_results[1].get_text(strip=True)
                if len(grant_results) > 1
                else "N/A",
                "Partner": partner.get_text(strip=True) if partner else "N/A",
            }
            print(f"Scraping project: {project_data['Partner']}")
            self.data.append(project_data)

    def scrape_all_projects(self) -> None:
        for link in self.links:
            self.scrape_project(link)

    def save_to_csv(self, file_name: str = "ikea_foundation_projects.csv") -> None:
        folder_path = os.path.abspath(os.path.join(os.getcwd(), "../..", "data"))

        # Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Specify the file path
        file_path = os.path.join(folder_path, file_name)
        df = pd.DataFrame(
            self.data,
            columns=[
                "URL",
                "Title",
                "Description",
                "Total Granted",
                "Total Paid",
                "Date Granted",
                "Geographic Area",
                "Partner",
            ],
        )
        df.to_csv(file_path, index=False)

        print(f"Scraping terminé. Les données ont été enregistrées dans '{file_path}'.")
