import json
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from PIL import Image

from apollo.chat import Chat
from apollo.VectorStore import VectorStore
from Create_yearly.src.one_governance.GenAI.Gen_full_class import (  # Replace 'your_module' with the name of the module that contains the DataGenerator class
    DataGenerator,
    get_binary_file_downloader_html,
    text_to_docx,
)
from Create_yearly.src.one_governance.utils import (
    filter_by_date,
    filter_by_date_2,
    get_report_period,
)


def main() -> None:
    # both false if you have alread computed all the project report
    create_project_report = (
        False  # to create the report for each project during the user exp
    )
    create_all_project_report = False  # to create all the report for each project at the beginning of the user exp
    one_shot = True  # si on veut ecrire le rapport en une fois et non par partie

    st.set_page_config(page_title="OneGovernance", layout="wide")

    # Write ikea project overwiew

    # Sidebar for navigation
    with st.sidebar:
        page = st.radio(
            "Select a page",
            [
                "Project Dashboard",
                "Foundation Report Generation",
                "Foundation Knowledge Hub",
            ],
        )
    # st.header("Select a page")
    # page = st.radio("", ["Yearly Report", "Appolo"])

    # Ouvrez l'image se trouvant en local
    image = Image.open("./data/White logo - no background.png")

    # Allows to choose the position of the logo for all pages
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image(image, caption="", use_column_width=False, width=150)

    if page == "Project Dashboard":
        st.header("Project Dashboard")
        col1_1, col1_2 = st.columns([1, 1])

        # Create a DataGenerator instance
        data_gen = DataGenerator()
        # Load the number of projects
        # nb_project = data_gen.nb_projects()

        # Get user input for nb_elem_base and nb_elem
        Demo = False  # st.checkbox("Demo")

        # Ask for the report type
        with col1_1:
            report_type = st.selectbox(
                "Please select the time frame for our analysis:",
                ("Yearly", "Quarterly", "Monthly"),
            )
        quarter = None
        month = None
        # Ask for the year
        with col1_2:
            year = st.number_input(
                "Enter the Year", min_value=2000, max_value=2023, step=1, value=2023
            )  # modify the min_value and max_value as per your requirement

        if report_type == "Quarterly":
            # Ask for the quarter if a quarterly report is selected
            quarter = st.selectbox(
                "Which quarter would you like to use for the report?",
                ("1st Quarter", "2nd Quarter", "3rd Quarter", "4th Quarter"),
            )
        elif report_type == "Monthly":
            # Ask for the month if a monthly report is selected
            month = st.selectbox(
                "Which month would you like to use for the report?",
                (
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
                ),
            )

        month_start, month_end = get_report_period(year, report_type, quarter, month)

        file_path = "./src/Create_yearly/data/data_gen/cleaned_project_data_full.csv"

        df = filter_by_date_2(file_path, month_start, month_end)

        # Group by the Date Choice and count the number of projects
        project_counts = df.groupby("Date Choice").size()
        st.write(df.shape[0], " projects found in the selected period.")
        ##################################################  TO FINISH  ###############################33

        # Tentative de conversion des colonnes en datetime
        df["9. Start date_analyse"] = pd.to_datetime(
            df["9. Start date_analyse"], errors="coerce"
        )
        df["10. End date_analyse"] = pd.to_datetime(
            df["10. End date_analyse"], errors="coerce"
        )

        print("x-------------------------------")
        print(type(df["9. Start date_analyse"]))
        print("-------------------------------")

        # Comparaison des budgets initiaux et des montants financés
        fig, ax = plt.subplots()
        ax.scatter(
                df["5. Total Budget_analyse"], df["6. Amount funded_analyse"], alpha=0.5
            )
        ax.set_xlabel("Total Budget")
        ax.set_ylabel("Amount Funded")
        ax.set_title("Budget vs Funded Amount")
        with st.expander("Budget vs. Funded Amount Comparison"): 
            st.pyplot(fig)

        # Répartition des projets selon leur durée
        project_duration = (
            df["10. End date_analyse"] - df["9. Start date_analyse"]
        ).dt.days

        fig, ax = plt.subplots()
        ax.hist(
            project_duration.dropna(), bins=30
        )  # Utilisation de dropna() pour éviter les NaN
        ax.set_title("Distribution of Project Durations")
        ax.set_xlabel("Duration (Days)")
        ax.set_ylabel("Number of Projects")
        with st.expander("Project Duration Distribution"):
            
            st.pyplot(fig)

        np.random.seed(0)  # pour avoir des résultats reproductibles
        goal_counts = pd.Series(
            np.random.randint(1, df.shape[0], 15),
            index=["goal " + str(i) for i in range(1, 16)],
        )

        # Créez la figure et l'axe
        fig, ax = plt.subplots()

        # Créez le graphique en camembert
        ax.pie(
            goal_counts,
            labels=goal_counts.index,
            autopct="%1.1f%%",
            colors=plt.cm.Dark2.colors,
        )
        ax.set_facecolor("none")

        # Affichez le graphique
        with st.expander("Goal category breakdown"):
            st.pyplot(fig)

        fig, ax = plt.subplots()
        project_counts.plot(kind="line", ax=ax)
        ax.set_xlabel("Date")
        ax.set_ylabel("number of projects")
        # ax.set_title('Titre du graphique')
        with st.expander("Project active over time"):
            st.pyplot(fig)

        ################################################################################

        # Boxplot des Budgets par Mois/Trimestre
        fig, ax = plt.subplots()
        sns.boxplot(
            x=df["9. Start date_analyse"].dt.to_period("M"),
            y="5. Total Budget_analyse",
            data=df,
            ax=ax,
        )
        ax.set_title("Monthly Budget Distribution")
        ax.set_xlabel("Month")
        ax.set_ylabel("Budget")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        ax.invert_xaxis()
        with st.expander("Budget Distribution by Period"):
            st.pyplot(fig)
        # Compter les occurrences de chaque catégorie géographique

        geography_counts = df["Continent"].value_counts()

        # Calculer les proportions
        geography_proportions = geography_counts / geography_counts.sum()

        fig, ax = plt.subplots()
        # Créer un bar plot pour les proportions
        geography_proportions.plot(kind="bar", color="skyblue", ax=ax)
        ax.set_title("Proportion of Projects by Geography")
        ax.set_xlabel("Geography")
        ax.set_ylabel("Proportion")
        # Rotation des étiquettes de l'axe x à la verticale pour une meilleure lisibilité
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

        # Ajouter des étiquettes de pourcentage sur chaque barre
        for p in ax.patches:
            ax.annotate(
                f"{p.get_height():.2%}",
                (p.get_x() + p.get_width() / 2.0, p.get_height()),
                ha="center",
                va="center",
                xytext=(0, 10),
                textcoords="offset points",
            )

        # Afficher le graphique dans Streamlit

        with st.expander("Proportion of Projects by Continent"):
            st.pyplot(fig)

        # Heatmap des Projets par Mois et Catégorie
        project_heatmap_data = pd.crosstab(
            df["9. Start date_analyse"].dt.month, df["Continent"]
        )
        fig, ax = plt.subplots()
        sns.heatmap(project_heatmap_data, annot=True, cmap="Blues", ax=ax)
        ax.set_title("Project Start Heatmap")
        ax.set_xlabel("Continent")
        ax.set_ylabel("Category")
        with st.expander("Project Start Heatmap by continent"):
            st.pyplot(fig)

    #################################################################################

    # st.write(df.shape[0], " projects found in the selected period.")
    elif page == "Foundation Report Generation":
        st.header("Foundation Report Generation 📈")
        only_part = st.checkbox("Check this box to choose a specific section to write.")

        col1_1, col1_2 = st.columns([1, 1])

        # Create a DataGenerator instance
        data_gen = DataGenerator()
        # Load the number of projects
        # nb_project = data_gen.nb_projects()

        # Get user input for nb_elem_base and nb_elem
        Demo = False  # st.checkbox("Demo")

        # Ask for the report type
        with col1_1:
            report_type = st.selectbox(
                "Which report would you like to generate?",
                ("Yearly", "Quarterly", "Monthly"),
            )
        quarter = None
        month = None
        # Ask for the year
        with col1_2:
            year = st.number_input(
                "Enter the Year", min_value=2000, max_value=2023, step=1, value=2023
            )  # modify the min_value and max_value as per your requirement
        file_path = "Create_yearly/data/data_gen/projects_report.csv"

        if report_type == "Quarterly":
            # Ask for the quarter if a quarterly report is selected
            quarter = st.selectbox(
                "Which quarter would you like to use for the report?",
                ("1st Quarter", "2nd Quarter", "3rd Quarter", "4th Quarter"),
            )

        elif report_type == "Monthly":
            # Ask for the month if a monthly report is selected
            month = st.selectbox(
                "Which month would you like to use for the report?",
                (
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
                ),
            )

        month_start, month_end = get_report_period(year, report_type, quarter, month)

        if not create_project_report:
            # here we add the columns date to the results project df
            file_path = "./src/Create_yearly/data/data_gen/projects_report.csv"
        #  df_v1 = pd.read_csv("Create_yearly/data/data_scrapped/ikea_foundation_projects.csv")
        #  df_ = pd.read_csv(file_path)
        #  df_["Date Choice"] = df_v1["Date Choice"]
        #
        # #df_.to_csv("Create_yearly/data/data_gen/projects_report.csv",index=False,)

        df = filter_by_date(file_path, month_start, month_end)

        # to create all the report:
        if create_project_report and create_all_project_report:
            df = pd.read_csv(file_path)

        # st.write(df.shape[0], " projects found in the selected period.")
        if Demo:  # elseif recreate_option == 'No':
            full_report = pd.read_csv(
                "./src/Create_yearly/data/data_gen/yearly_final.csv",
                header=None,
            )[0].values[0]

        header = "Report"
        if only_part:  # write the chosen part
            part_to_create = st.selectbox(
                "Which part of the report would you like to create?",
                (
                    "1 - Letter from the Chairperson/President",
                    "2 - Mission Statement",
                    "3 - Executive Summary",
                    "4 - Period in Review/Highlights",
                    "5 - Programs and Services Overview",
                    "6 - Financial Statements",
                    "7 - Fundraising Activities",
                    "8 - Volunteer Contributions",
                    "9 - Governance Information about the foundation's governance structure",
                    "10 - Future Outlook and Goals",
                    "11 - Acknowledgments and Appreciation ",
                    "12 - Contact Information ",
                ),
            )
            part_to_create_mapping = {
                "1 - Letter from the Chairperson/President": 1,
                "2 - Mission Statement": 2,
                "3 - Executive Summary": 3,
                "4 - Period in Review/Highlights": 4,
                "5 - Programs and Services Overview": 5,
                "6 - Financial Statements": 6,
                "7 - Fundraising Activities": 7,
                "8 - Volunteer Contributions": 8,
                "9 - Governance Information about the foundation's governance structure": 9,
                "10 - Future Outlook and Goals": 10,
                "11 - Acknowledgments and Appreciation": 11,
                "12 - Contact Information": 12,
            }
            header = part_to_create
            if st.button(f"Generate the part {part_to_create} of the report"):
                af1, af2, af3 = st.columns([1, 2, 1])
                with af2:
                    with st.spinner(
                        f"Generating the part {part_to_create} of the {report_type} report..."
                    ):
                        full_report = data_gen.generate_yearly_chosen_part(
                            report_type,
                            year,
                            df,
                            part_to_create_mapping[part_to_create] - 1,
                            quarter,
                            month,
                        )
                        st.success(
                            f"{part_to_create} of the report generated successfully!"
                        )
                # Display full report
                if "full_report" in locals():
                    st.subheader("Report")
                    st.write(full_report)

        elif not only_part:
            if st.button("Generate report"):
                if not Demo:
                    if one_shot and not only_part:
                        with st.spinner(f"Generating {report_type} report at once..."):
                            full_report = data_gen.write_yearly_in_one_shot(
                                report_type, year, df, quarter, month
                            )

                    else:
                        if create_project_report:
                            with st.spinner("Gathering project reports..."):
                                data_gen.generate_project_report_full(df)
                        with st.spinner(f"Generating {report_type} report..."):
                            if not create_project_report:
                                df_yearly_by_part = data_gen.generate_yearly_by_part(
                                    report_type, year, df, quarter, month
                                )
                            else:
                                df_yearly_by_part = data_gen.generate_yearly_by_part(
                                    report_type, year, df, quarter, month, True
                                )

                            full_report = data_gen.transform_response(df_yearly_by_part)
                    st.success(f"{report_type} report generated successfully!")
                elif Demo:  # elseif recreate_option == 'No':
                    full_report = pd.read_csv(
                        "./src/Create_yearly/data/data_gen/yearly_final.csv",
                        header=None,
                    )[0].values[0]
                    st.success("Yearly report generated successfully!")

                # Display full report
                if "full_report" in locals():
                    st.subheader(header)
                    st.write(full_report)

        # Summarize report
        # if st.button("Summarize Report"):
        #    with st.spinner("Summarizing report..."):
        #        summary = data_gen.summarize_report(full_report)
        #    st.success("Report summarized successfully!")

        # Display summary
        # if "summary" in locals():
        #    st.subheader("Summary")
        #    st.write(summary)

        # make changes to the yearly report ( the result are used in the show yearly)
        #if not only_part:
        full_report = pd.read_csv(
            "./src/Create_yearly/data/data_gen/yearly_final.csv", header=None
        )[0].values[0]
        

        if "full_report" in locals():
            res = full_report
            changes = st.text_area("Enter your wanted changes here...")
            if changes:
                # Affiche un spinner pendant l'exécution de la fonction rewrite_yearly
                with st.spinner("Text revision"):
                    res = data_gen.rewrite_yearly(changes, full_report)
                st.success("Text revised successfully!")
                st.write(res)

        # transform the output to pdf and give a link to download it
        if "full_report" in locals():
            full_report_text = res
            # file_format = st.sidebar.selectbox("Select file format", ["DOCX", "PDF"])
            # if file_format == "PDF":
            # output_full_pdf = "Create_yearly/data/data_gen/yearly_report.pdf"
            # text_to_pdf(full_report_text, "Yearly Report", output_full_pdf)
            #   output_full = output_full_pdf

            # elif file_format == "DOCX":
            output_full_docx = "./src/Create_yearly/data/data_gen/yearly_report.docx"
            text_to_docx(full_report_text, "Report", output_full_docx)
            # output_full = output_full_docx

            st.sidebar.markdown(
                get_binary_file_downloader_html(output_full_docx, "DOCX"),
                unsafe_allow_html=True,
            )
            # st.sidebar.markdown(   get_binary_file_downloader_html(output_full_pdf, "PDF"), unsafe_allow_html=True,)

    elif page == "Foundation Knowledge Hub":
        st.header("Foundation Knowledge Hub 📚")

        vector_store = VectorStore()

        if "delete_status" not in st.session_state:
            st.session_state.delete_status = ""

        # Initialize chat state
        if st.session_state.get("chat") is None:
            st.session_state.chat = Chat()

        chat = st.session_state.chat

        # Sidebar for document upload
        with st.sidebar:
            st.header("Upload Documents")
            uploaded_files = st.file_uploader(
                "Choose files (World, excel, PDF, TXT, csv)",
                type=["docx", "xlsx", "pdf", "txt", "csv"],
                accept_multiple_files=True,
            )
            if uploaded_files is not None:
                for uploaded_file in uploaded_files:
                    # Determine the file extension to handle file appropriately
                    file_type = uploaded_file.name.split(".")[-1].lower()
                    file_path = f"temp_file_{uploaded_file.name}"  # Name temp file with original name

                    # Write the uploaded file to a temporary file
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getvalue())

                    try:
                        if file_type == "pdf":
                            # Extract title from PDF and push the document
                            title = vector_store.extract_title(pdf_path=file_path)
                            vector_store.push_document(
                                document_path=file_path, title=title
                            )
                        elif file_type == "txt":
                            # Assume the first line of the text file is the title
                            title = vector_store.extract_title_from_csv(
                                pdf_path=file_path
                            )
                            vector_store.push_document(
                                document_path=file_path, title=title
                            )
                        elif file_type == "csv":
                            # Assume the first column of the first row could serve as the title
                            with open(file_path, "r") as f:
                                first_line = f.readline()
                                title = first_line.split(",")[0].strip()
                            vector_store.push_document(
                                document_path=file_path, title=title
                            )

                        elif file_type == "docx":
                            # Extract title from docx and push the document
                            title = vector_store.extract_title_from_docx(
                                docx_path=file_path
                            )
                            vector_store.push_document(
                                document_path=file_path, title=title
                            )
                        elif file_type == "xlsx":
                            # Extract title from xlsx and push the document
                            title = vector_store.extract_title_from_xlsx(
                                xlsx_path=file_path
                            )
                            vector_store.push_document(
                                document_path=file_path, title=title
                            )

                        st.success(
                            f"File '{uploaded_file.name}' uploaded successfully!"
                        )
                    except Exception as e:
                        st.error(
                            f"Failed to upload file '{uploaded_file.name}': {str(e)}"
                        )

                    os.remove(file_path)  # Clean up the temporary file after processing

            # Display documents in the index
            st.header("Uploaded Documents")
            for doc in vector_store.fetch_documents(max_results=20):
                col1, col2 = st.columns([0.8, 0.2])
                with col1:
                    metadata = json.loads(doc["metadata"])
                    st.text(metadata["title"])
                with col2:
                    if st.button("✖", key=doc["id"]):
                        result = vector_store.delete_document(doc["id"])
                        if isinstance(result, str) and len(result) > 0:  # Error case
                            st.session_state.delete_status = (
                                f"Failed to delete document: {result}"
                            )
                        else:
                            st.session_state.delete_status = (
                                "Document deleted successfully!"
                            )
                            st.rerun()  # Rerun to refresh the document list

        st.sidebar.text(st.session_state.delete_status)

        # Handle chat and user interaction
        for message in chat.messages:
            if isinstance(message, HumanMessage):
                with st.chat_message("user"):
                    st.write(message.content)
            elif isinstance(message, AIMessage):
                with st.chat_message("assistant"):
                    st.write(message.content)

        prompt = st.chat_input("Say something...")
        if prompt:
            with st.spinner("..."):
                chat.add_message(prompt)
                st.rerun()


if __name__ == "__main__":
    main()
