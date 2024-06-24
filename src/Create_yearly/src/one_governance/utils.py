import pandas as pd


def get_report_period(
    year: int, report_type: str, quarter: str = None, month: str = None
) -> tuple:
    start_date, end_date = None, None

    if report_type == "Yearly":
        start_date = pd.Timestamp(year, 1, 1)  # Start of the year
        end_date = pd.Timestamp(year, 12, 1)  # End of the year

    if report_type == "Quarterly":
        if quarter == "1st Quarter":
            start_date = pd.Timestamp(year, 1, 1)
            end_date = pd.Timestamp(year, 3, 1)
        elif quarter == "2nd Quarter":
            start_date = pd.Timestamp(year, 4, 1)
            end_date = pd.Timestamp(year, 6, 1)
        elif quarter == "3rd Quarter":
            start_date = pd.Timestamp(year, 7, 1)
            end_date = pd.Timestamp(year, 9, 1)
        elif quarter == "4th Quarter":
            start_date = pd.Timestamp(year, 10, 1)
            end_date = pd.Timestamp(year, 12, 1)

    if report_type == "Monthly":
        month_number = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ].index(month) + 1
        start_date = pd.Timestamp(year, month_number, 1)  # Start of the month
        end_date = pd.Timestamp(year, month_number, 1)  # End of the month

    return start_date.to_pydatetime(), end_date.to_pydatetime()


import pandas as pd


def filter_by_date(file_path, start_date, end_date) -> pd.DataFrame:
    # Convertir les dates en datetime object avec l'année et le mois
    start_date = pd.to_datetime(start_date).to_period("M")
    end_date = pd.to_datetime(end_date).to_period("M")

    # Lire le df à partir du fichier csv
    df = pd.read_csv(file_path)

    # Vérifie si 'date_chois' est une colonne dans le dataframe
    if "Date Choice" in df.columns:
        df["Date Choice"] = pd.to_datetime(df["Date Choice"]).dt.to_period(
            "M"
        )  # Convertir la colonne date_chois en datetime avec juste l'année et le mois
        # Filtrer sur les lignes où date_chois est entre la date de début et de fin
        return df[(df["Date Choice"] >= start_date) & (df["Date Choice"] <= end_date)]
