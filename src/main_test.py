import streamlit as st
import pandas as pd
import json
import os
from langchain_core.messages import AIMessage, HumanMessage
from apollo.chat import Chat
from apollo.VectorStore import VectorStore

import tempfile
import base64
from Create_yearly.src.one_governance.GenAI.Gen_full_class import DataGenerator,get_binary_file_downloader_html, text_to_pdf  # Replace 'your_module' with the name of the module that contains the DataGenerator class



def main():
    st.set_page_config(page_title="Apollo", layout="wide")
    st.title("OneGovernance - AI tools for foundations.")

    # Sidebar for navigation
    with st.sidebar:
        page = st.radio("Select a page", ["Yearly Report", "Appolo"])
    #st.header("Select a page")
    #page = st.radio("", ["Yearly Report", "Appolo"])

    if page == "Yearly Report":
        st.header("Yearly Report Generation")

        # Create a DataGenerator instance
        data_gen = DataGenerator()
        # Load the number of projects
        nb_project = data_gen.nb_projects()

        # Get user input for nb_elem_base and nb_elem
        nb_elem_base = st.number_input("Enter the number of projects to create from scraped data", min_value=1, max_value=nb_project-1, value=3)
        nb_elem = st.number_input("Enter the number of projects report to write", min_value=1, max_value=nb_elem_base, value=1)

        df_projects_report = pd.read_csv("/home/peyron/Documents/Prometee/onegovernance-apollo/src/Create_yearly/data/data_gen/projects_report.csv")
        nb_projects = df_projects_report.shape[0]
        

        # Generate project reports and if the project are already created display a success message
        if st.button("Generate Project Reports"):
            if nb_elem_base > nb_projects:
                with st.spinner("Generating project reports..."):
                    data_gen.generate_project_report_full(nb_elem_base, nb_elem)
                st.success("Project reports generated successfully!")
            else:
                st.success("Project reports generated successfully!")

        # Generate yearly report by part
        df_yearly_by_part = pd.read_csv("/home/peyron/Documents/Prometee/onegovernance-apollo/src/Create_yearly/data/data_gen/yearly_by_part.csv")
    
        recreate_option = st.radio("Do you want to recreate the Yearly Report?", options=['Yes', 'No'], index=1)
        if recreate_option == 'Yes':
            with st.spinner("Generating yearly report by part..."):
                df_yearly_by_part = data_gen.generate_yearly_by_part()
                full_report = data_gen.transform_response(df_yearly_by_part)
            st.success("Yearly report generated successfully!")
        else: #elseif recreate_option == 'No':
            st.success("Using existing yearly report.")  
            full_report = pd.read_csv("/home/peyron/Documents/Prometee/onegovernance-apollo/src/Create_yearly/data/data_gen/yearly_final.csv", header=None)
    


        # Display full report
        if 'full_report' in locals():
            if st.checkbox("Show Full Report"):
                st.subheader("Full Report")
                st.write(full_report[0].values[0])

            # Summarize report
            if st.button("Summarize Report"):
                with st.spinner("Summarizing report..."):
                    summary = data_gen.summarize_report(full_report)
                st.success("Report summarized successfully!")

            # Display summary
        if 'summary' in locals():
                st.subheader("Summary")
                st.write(summary)

        if 'full_report' in locals() and 'summary' in locals():
                full_report_text = full_report[0].values[0]
                summary_text = str(summary)
                output_full ="/home/peyron/Documents/Prometee/onegovernance-apollo/src/Create_yearly/data/data_gen/yearly_report.pdf"
                output_summary = "/home/peyron/Documents/Prometee/onegovernance-apollo/src/Create_yearly/data/data_gen/yearly_report_summary.pdf"
                text_to_pdf(full_report_text,"Yearly Report", output_full )
                text_to_pdf(summary_text,"Yearly Report Summary", output_summary )
                # Set path to your PDF file

                # Give download link for the PDF
                st.markdown(get_binary_file_downloader_html(output_full, 'PDF'), unsafe_allow_html=True)


    elif page == "Appolo":
        st.header("Apollo - AI Specialized in Commodities.")

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
                "Choose files (PDF, TXT, csv, json)", type=["pdf", "txt", "csv", "json"], accept_multiple_files=True
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
                            vector_store.push_document(document_path=file_path, title=title)
                        elif file_type == "txt":
                            # Assume the first line of the text file is the title
                            with open(file_path, "r") as f:
                                title = f.readline().strip()
                            vector_store.push_document(document_path=file_path, title=title)
                        elif file_type == "csv":
                            # Assume the first column of the first row could serve as the title
                            with open(file_path, "r") as f:
                                first_line = f.readline()
                                title = first_line.split(',')[0].strip()
                            vector_store.push_document(document_path=file_path, title=title)
                            
                        elif file_type == "json":
                            # Assume a top-level key named 'title' or 'name' serves as the document title
                            with open(file_path, 'r') as file:
                                data = json.load(file)
                                title = data.get('title') or data.get('name') or "Untitled Document"
                            vector_store.push_document(document_path=file_path, title=title)

                        st.success(f"File '{uploaded_file.name}' uploaded successfully!")
                    except Exception as e:
                        st.error(f"Failed to upload file '{uploaded_file.name}': {str(e)}")

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



