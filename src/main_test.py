import json
import os

import pandas as pd
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from PIL import Image

from apollo.chat import Chat
from apollo.VectorStore import VectorStore
from Create_yearly.src.one_governance.GenAI.Gen_full_class import (  # Replace 'your_module' with the name of the module that contains the DataGenerator class
    DataGenerator,
    get_binary_file_downloader_html,
    text_to_docx,
    text_to_pdf,
)
from Create_yearly.src.one_governance.utils import filter_by_date, get_report_period, filter_by_date_2


def main() -> None:
    #both false if you have alread computed all the project report
    create_project_report = False # to create the report for each project during the user exp
    create_all_project_report = False # to create all the report for each project at the beginning of the user exp
    one_shot = True # si on veut ecrire le rapport en une fois et non par partie

    st.set_page_config(page_title="Apollo", layout="wide")

    # Write ikea project overwiew 

    # Sidebar for navigation
    with st.sidebar:
        page = st.radio(
            "Select a page", ["Report overview", "Ikea foundation: Knowledge Hub", "Yearly Report generation"]
        )
    # st.header("Select a page")
    # page = st.radio("", ["Yearly Report", "Appolo"])

    # Ouvrez l'image se trouvant en local
    image = Image.open(
        "../data/White logo - no background.png"
    )

    # Allows to choose the position of the logo for all pages
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image(image, caption="", use_column_width=False, width=150)


    if page =="Report overview":
        st.header("IKEA report overview")
        col1_1, col1_2 = st.columns([1, 1])

        # Create a DataGenerator instance
        data_gen = DataGenerator()
        # Load the number of projects
        #nb_project = data_gen.nb_projects()

        # Get user input for nb_elem_base and nb_elem
        Demo = False #st.checkbox("Demo")

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

        file_path = "Create_yearly/data/data_gen/filled_projects.csv"
    


        df = filter_by_date_2(file_path, month_start, month_end)
        ##################################################  TO FINISH  ###############################33
        ## Faire une fonction transforamnt certaine colonne du df en info type nombre ou autre pour pouvoir être analysé
        #df = clean_trasform_data(df, month_start, month_end)

        #### Afficher des infos interessant
        st.write(df['Date Choice'])
        
    
        # Group by the Date Choice and count the number of projects
        project_counts = df.groupby('Date Choice').size()

        # Plot the data
        st.line_chart(project_counts)

        st.write(df.shape[0], " projects found in the selected period.")

        #st.write(df.shape[0], " projects found in the selected period.")
    elif page == "Yearly Report generation":
        st.header("Summary of Yearly Report 📈")
        col1_1, col1_2 = st.columns([1, 1])

        # Create a DataGenerator instance
        data_gen = DataGenerator()
        # Load the number of projects
        #nb_project = data_gen.nb_projects()

        # Get user input for nb_elem_base and nb_elem
        Demo = False #st.checkbox("Demo")

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
            #here we add the columns date to the results project df
            file_path = "Create_yearly/data/data_gen/projects_report.csv"
          #  df_v1 = pd.read_csv("Create_yearly/data/data_scrapped/ikea_foundation_projects.csv")
          #  df_ = pd.read_csv(file_path)
          #  df_["Date Choice"] = df_v1["Date Choice"]
          #
          # #df_.to_csv("Create_yearly/data/data_gen/projects_report.csv",index=False,)

    
        df = filter_by_date(file_path, month_start, month_end)


            
        #to create all the report: 
        if create_project_report and create_all_project_report:
            df = pd.read_csv(file_path)

        st.write(df.shape[0], " projects found in the selected period.")
        if Demo:  # elseif recreate_option == 'No':
                full_report = pd.read_csv(
                    "Create_yearly/data/data_gen/yearly_final.csv",
                    header=None,
                )[0].values[0]

        if st.button("Generate report"):
            if not Demo:
                if one_shot:
                    with st.spinner(f"Generating {report_type} report at once..."):
                        full_report = data_gen.write_yearly_in_one_shot(
                            report_type, year,df, quarter, month) 

                else:
                    if create_project_report :
                        with st.spinner("Gathering project reports..."):
                            data_gen.generate_project_report_full(df)
                    with st.spinner(f"Generating {report_type} report..."):
                        if not create_project_report:
                            df_yearly_by_part = data_gen.generate_yearly_by_part(
                            report_type, year,df, quarter, month)
                        else: 
                            df_yearly_by_part = data_gen.generate_yearly_by_part(
                            report_type, year,df, quarter, month, True)

                        full_report = data_gen.transform_response(df_yearly_by_part)
                st.success("Yearly report generated successfully!")
            elif Demo:  # elseif recreate_option == 'No':
                full_report = pd.read_csv(
                    "Create_yearly/data/data_gen/yearly_final.csv",
                    header=None,
                )[0].values[0]
                st.success("Yearly report generated successfully!")

            # Display full report
            if "full_report" in locals():
                st.subheader("Full Report")
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
        if "full_report" in locals():
            res = full_report
            changes = st.text_area("Enter you wanted changes here...")
            if changes:
                # Affiche un spinner pendant l'exécution de la fonction rewrite_yearly
                with st.spinner("Text revision"):
                    res = data_gen.rewrite_yearly(changes, full_report)
                st.success("Text revised successfully!")
                st.write(res)

        # transform the output to pdf and give a link to download it
        if "full_report" in locals():
            full_report_text = res
            file_format = st.sidebar.selectbox("Select file format", ["DOCX", "PDF"])

            if file_format == "PDF":
                output_full_pdf = "Create_yearly/data/data_gen/yearly_report.pdf"
                text_to_pdf(full_report_text, "Yearly Report", output_full_pdf)
                output_full = output_full_pdf

            elif file_format == "DOCX":
                output_full_docx = "Create_yearly/data/data_gen/yearly_report.docx"
                text_to_docx(full_report_text, "Yearly Report", output_full_docx)
                output_full = output_full_docx

            st.sidebar.markdown(
                get_binary_file_downloader_html(output_full, file_format),
                unsafe_allow_html=True,
            )

    elif page == "Ikea foundation: Knowledge Hub":
        st.header("IKEA foundation: Knowledge Hub 📚")

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
