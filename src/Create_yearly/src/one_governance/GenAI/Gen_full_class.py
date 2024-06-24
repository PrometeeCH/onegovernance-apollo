import base64
import csv
import datetime
import os

import pandas as pd
from fpdf import FPDF
from openai import AzureOpenAI


class DataGenerator:
    def __init__(self) -> None:
        self.client = AzureOpenAI(
            api_key=os.environ["AZURE_OPENAI_API_KEY_CHAT"],
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT_CHAT"],
            api_version=os.environ["AZURE_OPENAI_API_VERSION_CHAT"],
        )

    def create_template(
        self,
        case: int,
        project_data: str,
        previous_part: str,
        general_info: str,
        template_part: str,
    ) -> str:
        if case == 1:  # case for yearly report project_report_gen_data.py
            today = datetime.date.today().strftime("%Y-%m-%d")
            prompt = f""" Generate synthetic information for a project. Use the current available information( if you can found it after project data:), otherwise, generate the information needed.
                        Note that in the following we specify the available and not available data. Here are the specifics:

                        1. Project name: available. (put a marker [x] here)
                        2. Geography: Specify continent, country, and city. If not available, generate a plausible location.
                        3. UN Goal: Accordingly to the project data you have Choose from the 17 UN Goals. not specified, generate a suitable goal  (don't put a marker [x] here). here are the 17 UN Goals you can choose from: GOAL 1. No Poverty GOAL 2. Zero Hunger GOAL 3. Good Health and Well-being GOAL 4. Quality Education GOAL 5: Gender Equality GOAL 6. Clean Water and Sanitation GOAL 7. Affordable and Clean Energy GOAL 8. Decent Work and Economic Growth GOAL 9. Industry, Innovation and Infrastructure GOAL 10. Reduced Inequality GOAL 11. Sustainable Cities and Communities GOAL 12. Responsible Consumption and Production GOAL 13. Climate Action GOAL 14. Life Below Water GOAL 15. Life on Land GOAL 16. Peace and Justice Strong Institutions GOAL 17. Partnerships to achieve the Goal
                        4. Type of giving: Choose from the 9 specified types according to the project data given(don't put a marker [x] here). here are the 9 types you can choose from:1. Traditional Philanthropy 2. Donor-Advised Funds (DAFs) 3. Corporate Social Responsibility (CSR) 4. Community Investing 5. Venture Philanthropy 6. Program-Related Investments (PRIs) 7. Impact Investing: 8. Social Bond Principles (SBP) 9. Environmental, Social, and Governance (ESG) Investing
                        5. Total Budget: available, amount in USD. (put a marker [x] here)
                        6. Amount funded: available, amount in USD. (put a marker [x] here)
                        7. Amount still to be funded: not available, generate a plausible amount in USD.  (put a marker [x] here)
                        8. Distribution type: Choose from 'Per project', 'Per request', 'Scheduled'. not specified, generate a suitable type.(don't put a marker [x] here)
                        9. Start date: available, generate a plausible start date.(put a marker [x] here)
                        10. End date: not available, generate a plausible end date.(don't put a marker [x] here)
                        11. Our contribution to this project: not available, generate a plausible percentage.(don't put a marker [x] here)
                        12. Funding status: Open or Closed. not specified, choose a suitable status.(don't put a marker [x] here)
                        13. Partnerships sponsor(s): If not available, generate plausible sponsor(s) and their percentage contribution.(put a marker [x] here)
                        14. Partnerships project manager: If not available, generate a plausible manager's name.(don't put a marker [x] here)
                        15. Partnerships consultant: If not available, generate a plausible consultant's name/company.(don't put a marker [x] here)
                        16. Results objectives (KPI): If not available, generate a plausible objectives.(don't put a marker [x] here)
                        17. Latest review SWOT Strength: not available, generate a plausible strength.(don't put a marker [x] here)
                        18. Latest review SWOT Weaknesses: not available, generate a plausible weakness.(don't put a marker [x] here)
                        19. Latest review SWOT Opportunity: not available, generate a plausible opportunity.(don't put a marker [x] here)
                        20. Latest review SWOT Threat: not available, generate a plausible threat.(don't put a marker [x] here)
                        21. Latest review comments: not available, generate plausible comments.(don't put a marker [x] here)
                        22. Satisfaction Ranking overall: not available, generate a plausible ranking.(don't put a marker [x] here)
                        23. Satisfaction Ranking overall Strat: not available, generate a plausible ranking.(don't put a marker [x] here)
                        24. Satisfaction Ranking overall partners: not available, generate a plausible ranking.(don't put a marker [x] here)
                        25. Satisfaction Ranking overall organisation & processes: not available, generate a plausible ranking.(don't put a marker [x] here)
                        26. Satisfaction Ranking overall communication: not available, generate a plausible ranking.(don't put a marker [x] here)
                        27. Satisfaction comments: not available, generate plausible comments.(don't put a marker [x] here)
                        28. Other comments: not available, generate plausible comments.(don't put a marker [x] here)
                        29. Author: not available, generate a plausible author's name.(don't put a marker [x] here)
                        30. Date of last update: not available, generate a plausible date the data must be prior to the date of {today}.(don't put a marker [x] here)
                        31. Contact details: not available, generate a plausible email address.(don't put a marker [x] here)

                        Fill in the information for each of these categories, and mark the data that you found thanks to the project data with [x],(probably point 1,5,6,7,9) .

                        project data: {project_data}

                        the generated or found information should never be "not available" because if they are you should generate them.
                        """

        elif case == 2:  # case for project report project_report_gen.py
            prompt = f"""I want you to be a project report writer reporter for a foundation.
                        In the following case you will write for the ikea foundation projects.
                        Write a project report with the following data about the project:
                        {project_data}
                        For the data with a marker [x] you must add the marker in the text(right after the info or at the end of the sentence). This is to specify that the data used has not been generated(it is real data).
                        I just want the project report to be written in a professional way. without adding any explanation or anything else. But it must be writen in a way that it is a report. not just a list of data.

                        The report must be as the following exemple with the info addaptaded for the data of the project:

                        PROJECT REPORT

                        Title: Donation: Africa Private Sector Forum on Forced Displacement 2023 [x]

                        Geographical Scope: This initiative is primarily focused on Africa, with the specific country and city yet to be defined [x].

                        UN Goal: Aligned with the United Nations' Goal 8, the project endeavors to promote Decent Work and Economic Growth [x].

                        Type of Giving: The project follows the model of Traditional Philanthropy [x].

                        Budget Overview: With a total budget of $500,000 [x], the project has already secured $300,000 [x] in funding, leaving $200,000 [x] yet to be funded.

                        Distribution Type: The funding will be distributed per project [x].

                        Project Timeline: The project is set to commence in May 2023 [x] and is slated for completion by December 2023.

                        Contribution: Our foundation has contributed 60% of the current funding [x].

                        Funding Status: At present, the project's funding status remains open [x].

                        Partnerships: The project is supported by the IKEA Foundation (40%), UNHCR (20%), and the African Entrepreneur Collective (40%) [x]. The project's management is led by Abigail Nkomo, with consultation provided by Amahoro Consultancy Services [x].

                        Key Performance Indicators: The project aims to engage at least 100 private sector actors and secure 50 new commitments from businesses to support displaced communities [x].

                        SWOT Analysis:
                        Strengths - Strong coalition of partners with diverse strengths and resources [x].
                        Weaknesses - Difficulties in coordinating between different partners and stakeholders [x].
                        Opportunities - High potential for impact by involving the private sector in addressing forced displacement [x].
                        Threats - Potential lack of interest or commitment from private sector actors [x].

                        Review Comments: The project shows potential but requires stronger engagement strategies to attract private sector actors [x].

                        Satisfaction Ranking: The project has received an overall satisfaction ranking of 7/10 [x]. The strategic satisfaction ranking is 8/10 [x], while the partners and organization & processes have scored 6/10 and 7/10 respectively [x]. The communication has also been ranked at 7/10 [x].

                        Satisfaction Comments: Overall, partners are satisfied with the progress but are optimistic about improving the project further [x].

                        Additional Comments: The forum provides a unique platform to address forced displacement issues but requires more focused strategies [x].

                        Author: This report has been compiled by Josephine Tendai [x].

                        Date of the Last Update: June 2, 2024 [x].

                        Contact Details: Josephine can be reached at j.tendai@africaprivatesectorforum.org [x].

                        Project Description: The IKEA Foundation is supporting the African Entrepreneur Collective, in collaboration with the Amahoro Coalition and UNHCR, to host the second African Private Sector Forum for Refugees. Through this forum, the partners aim to build on and amplify the need to engage private sector actors in displacement setting [x].

                        """
        elif case == 3:  # case for yearly report yearly_report_gen_by_part.py
            prompt = f"""As a yearly report writer for the IKEA Foundation, your task is to compose a section of the annual report. The section you provide must be precise. Please follow the structured guidance provided below:

                        1. Section Overview: First, here is a brief explanation of the specific part of the report you are tasked to write:
                        {template_part}

                        2. Project Data: Review the data from projects funded by the foundation over the past year. Use this information to highlight key achievements and progress:
                        {project_data}
                        Note: This is the end of the project data.

                        3. Foundation Overview: Incorporate the following general information about the foundation to provide context and factual background in your report:
                        {general_info}
                        Note: This is the end of the general information.

                        All data should be presented in a professional manner. For data marked with [x], include this marker in your text right after the relevant information or at the end of the sentence to emphasize its importance.

                        Continuity in Reporting:
                        Finally, note that you are crafting a segment of a larger document. To maintain a cohesive and comprehensive narrative, refer to the section written previously:
                        {previous_part}

                        This previous part provides essential context, ensuring that your contribution is integrated smoothly without duplicating content. Use this context to enhance the flow and coherence of the report, contributing unique insights or information that progresses the narrative logically.
                        For each part, write the title of the part at the beginning of the text.

                        """

        return prompt

    def get_response(self, prompt_: str) -> str:
        response = self.client.chat.completions.create(
            model="Gpt-4-onegovernance",
            messages=[{"role": "user", "content": prompt_}],
            max_tokens=1900,
            temperature=0.7,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["###"],
        )
        last_response = response.choices[0].message.content
        if not last_response:
            return "No data generated"
        else:
            return str(last_response)

    def create_dict_from_text(self, text: str, description: str) -> dict:
        lines = text.split("\n")  # Split the text into lines
        result_dict = {}  # Initialize an empty dictionary
        for line in lines:  # For each line in the text
            if ":" in line:  # If the line contains a ':'
                key, value = line.split(":", 1)  # Split the line into key and value
                result_dict[
                    key.strip()
                ] = value.strip()  # Add the key-value pair to the dictionary
        result_dict["32. Description"] = description
        return result_dict  # Return the resulting dictionary

    def generate_project_data(self, df: pd.DataFrame) -> None:
        # Load projects from CSV
        df_projects = df

        # Process each project
        results = []
        for index, row in df_projects.iterrows():
            project_info = row.to_json()
            prompt_template = self.create_template(
                1, project_info, "previous_part", "general_info", "template_part"
            )
            filled_info = self.get_response(prompt_template)
            filled_infoo = self.create_dict_from_text(filled_info, row.Description)
            results.append(filled_infoo)

        # Save results to CSV
        df_results = pd.DataFrame(results)
        df_results.to_csv(
            "/home/peyron/Documents/Prometee/onegovernance-apollo/src/Create_yearly/data/data_gen/filled_projects.csv",
            index=False,
        )

    def generate_project_report(self) -> None:
        # Load projects from CSV
        df_projects = pd.read_csv(
            "/home/peyron/Documents/Prometee/onegovernance-apollo/src/Create_yearly/data/data_gen/filled_projects.csv"
        )

        # Process each project
        results = []
        for index, row in df_projects.iterrows():
            project_data = row.to_json()
            prompt = self.create_template(
                2, project_data, "previous_part", "general_info", "template_part"
            )
            filled_info = self.get_response(prompt)
            results.append(filled_info)

        # Save results to CSV
        df_results = pd.DataFrame(results, columns=["Filled Project Report"])
        df_results.to_csv(
            "/home/peyron/Documents/Prometee/onegovernance-apollo/src/Create_yearly/data/data_gen/projects_report.csv",
            index=False,
        )

    def generate_project_report_full(self, df: pd.DataFrame) -> None:
        self.generate_project_data(df)
        self.generate_project_report()

    def generate_yearly_by_part(self, nb_elem: int) -> pd.DataFrame:
        # Load data from CSV
        df_general_info = pd.read_csv(
            "/home/peyron/Documents/Prometee/onegovernance-apollo/src/Create_yearly/data/data_scrapped/yearly_report_data.csv"
        )
        df_projects_report = pd.read_csv(
            "/home/peyron/Documents/Prometee/onegovernance-apollo/src/Create_yearly/data/data_gen/projects_report.csv"
        )
        df_annal_template = pd.read_csv(
            "/home/peyron/Documents/Prometee/onegovernance-apollo/src/Create_yearly/data/data_scrapped/annualrewiew_template.csv"
        )

        # Get the data of the right form
        project_info = df_projects_report.head(nb_elem).to_string(index=False)
        general_info = df_general_info.to_string(index=False)

        # Process each part
        yearly_parts: list[str] = []
        for index, part in df_annal_template.iterrows():
            case_0 = "this is the first part we are creating hence no previous part"
            if index == 0:
                prompt = self.create_template(
                    3, project_info, case_0, general_info, part["contenu"]
                )
            else:
                prompt = self.create_template(
                    3,
                    project_info,
                    yearly_parts[index - 1],
                    general_info,
                    part["contenu"],
                )
            response = self.get_response(prompt)
            yearly_parts.append(response)

        # Save results to CSV
        df_yearly_report = pd.DataFrame(
            {"partie": df_annal_template.index + 1, "contenu": yearly_parts}
        )
        df_yearly_report.to_csv(
            "/home/peyron/Documents/Prometee/onegovernance-apollo/src/Create_yearly/data/data_gen/yearly_by_part.csv",
            index=False,
        )
        return df_yearly_report

    def transform_response(self, df_yearly_report: str) -> str:
        # df_yearly_report = pd.read_csv("../../../data/data_gen/yearly_by_part.csv")
        # start_time = time.time()
        combined_string = " ".join(df_yearly_report["contenu"])  # type: ignore

        prompt = f"""Task:I want you to transform a Yearly Report writen not continously by part into a Continuous Narrative with part.

                    Input Text, the yearly report writen by part:{combined_string}

                    Objective: i want you to rewrite the provided yearly report (input text) into a cohesive, continuous yearly report. Avoid redundancy and ensure smooth transitions between sections.

                    Instructions:

                    1. Eliminate Redundancies: Identify and remove repeated information.
                    2. Ensure Smooth Transitions: Link sections seamlessly without summarizing at transitions. you can put a tiltle for each section as you will have in the writen by part version.
                    3. Maintain Professional Tone: Keep the tone formal and suitable for stakeholders.
                    4. Review for Flow and Accuracy: Ensure the narrative flows logically and retains all factual data accurately.
                    5. For each part the new and olv versionmust be approximately the same length.

                    Your rewrite should create a streamlined, logically coherent report that communicates effectively without unnecessary repetition.

                    The final result should be a continuous narrative that flows logically from one section to the next and must be as precise and profesional as you can, do not try to be succint, be precise.
                    The final result must be composed of 12 part with their titles. For each part of the yearly report, the context and info are in the Input Text. Here are the name of the different part.
                    1. Letter from the Chairperson/President:
                    2. Mission Statement:
                    3. Executive Summary:
                    4. Year in Review/Highlights:
                    5. Programs and Services Overview:
                    6. Financial Statements:
                    7. Fundraising Activities:
                    8. Volunteer Contributions:
                    9. Governance Information:
                    10. Future Outlook and Goals:
                    11. Acknowledgments and Appreciation:
                    12. Contact Information:
                    I want all of them in the final result.
                    """
        reponse = self.get_response(prompt)

        # Chemin du fichier CSV
        output_file = "/home/peyron/Documents/Prometee/onegovernance-apollo/src/Create_yearly/data/data_gen/yearly_final.csv"

        # Écriture dans le fichier CSV
        self.to__csv(output_file, reponse)

        return reponse

    def rewrite_yearly(self, changes: str, full_report: str) -> str:
        prompt = f"""As a yearly report editor, you're tasked with modifying the following report: {full_report}.
        The requested modifications are as follows: {changes}.
        Please ensure these adjustments are both accurate and closely aligned with the original content.
        It's important to note that these changes are your top priority.
        All information from the original yearly report should be retained in the revised version, unless specified otherwise in the requested changes.
        """
        response = self.get_response(prompt)
        output_file = "/home/peyron/Documents/Prometee/onegovernance-apollo/src/Create_yearly/data/data_gen/yearly_final_r.csv"
        self.to__csv(output_file, response)

        return response

    def summarize_report(self, report: str) -> str:
        # Load the report from CSV
        # df_report = pd.read_csv("../../../data/data_gen/yearly_final.csv")
        # start_time = time.time()
        combined_string = report

        prompt = f"""Input Text, the yearly report written by part:{combined_string}

                Objective: i want you to return a shorter version of the input yearly report. Generate a structured, condensed version of the provided yearly report that maintains the original layout and captures essential information in a professional format. Write only the text summarized nothing else, for exemple do not write (Condensed Yearly Report:) but write directly the condensed report.

                Instructions:

                1. Retain Structure: Preserve the original part-by-part structure in the condensation process.
                2. Identify Crucial Content: Select and condense the essential details from each section of the report.
                3. Maintain Professional Tone: The condensed version must be formal and suitable for stakeholders.
                4. Ensure Accuracy: Keep all factual information from the original text intact.

                The final condensed version should provide a succinct, informative overview of the yearly report while maintaining the format and essence of the original. Each section of the condensed report should be concise, yet comprehensive, capturing the key details from the respective sections of the original.

                The final condensed version should be approximately 20 sentences in length, spread structurally across the respective sections.
 """

        response = self.get_response(prompt)

        # Chemin du fichier CSV
        output_file = "/home/peyron/Documents/Prometee/onegovernance-apollo/src/Create_yearly/data/data_gen/yearly_summary.csv"

        # Écriture dans le fichier CSV
        self.to__csv(output_file, response)

        return response

    # fonction ######################################
    def nb_projects(self) -> int:
        df = pd.read_csv(
            "/home/peyron/Documents/Prometee/onegovernance-apollo/src/Create_yearly/data/data_scrapped/ikea_foundation_projects.csv"
        )
        return int(df.shape[0])

    def to__csv(
        self, output_file: str, reponse: str
    ) -> None:  # Écriture dans le fichier CSV
        with open(output_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # Écrire la chaîne dans une ligne du CSV
            writer.writerow([reponse])


def get_binary_file_downloader_html(bin_file: str, file_label: str = "File") -> str:
    with open(bin_file, "rb") as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    bin_file = os.path.basename(bin_file)
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{bin_file}">Download {file_label}</a>'
    return href


class PDF(FPDF):
    def header(self) -> None:
        pass

    def footer(self) -> None:
        self.set_y(-15)
        self.set_font("Times", "I", 8)
        self.cell(0, 10, "Page %s" % self.page_no(), 0, 0, "C")


def text_to_pdf(input_string: str, header: str, output_filename: str) -> None:
    pdf = PDF()
    pdf.set_right_margin(10)
    pdf.set_left_margin(10)

    pdf.set_font("Times", "", 12)
    pdf.add_page()

    # Set header
    pdf.set_font("Times", "B", 14)
    pdf.cell(0, 10, header, ln=True, align="C")

    # Set font back to normal
    pdf.set_font("Times", "", 12)

    input_string = input_string.replace("€", " EUR")
    pdf.multi_cell(0, 10, input_string)

    pdf.output(output_filename)
