import datetime
import os
import datetime
import csv
import time
import argparse

import pandas as pd
from openai import AzureOpenAI

# Configure the AzureOpenAI client
client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY_CHAT"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT_CHAT"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION_CHAT"],
)

def create_template(case:int, project_data: str, previous_part:str, general_info: str, template_part:str ) -> str:
    
    if case == 1:# case for yearly report project_report_gen_data.py
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
    
    elif case == 2:# case for project report project_report_gen.py
        prompt = f"""I want you to be a project report writer reporter for a foundation.
                    In the following case you will write for the ikea foundation projects.
                    Write a project report with the following data about the project:
                    {project_data}
                    For the data with a marker [x] you must add the marker in the text(right after the info or at the end of the sentence). This is to specify that the data used has not been generated(it is real data).
                    I just want the project report to be written in a professional way. without adding any explanation or anything else. But it must be writen in a way that it is a report. not just a list of data.
                    """
    elif case == 3:# case for yearly report yearly_report_gen_by_part.py
        prompt = f"""As a yearly report writer for the IKEA Foundation, your task is to compose a section of the annual report. Please follow the structured guidance provided below:

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

def get_response(prompt_: str) -> str:
    response = client.chat.completions.create(
        model="Gpt-4-onegovernance",
        messages=[{"role": "user", "content": prompt_}],
        max_tokens=1500,
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
        return str(last_response)  # Attention


####rvoir cette fonction pb avce les 4 Ranking overall
def create_dict_from_text(text: str, description: str) -> dict:
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

def write_to_csv(response: str, output_file: str) -> None:
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Response"])  # Write header
        writer.writerow([response])  # Write data
##########################Start of the generation##########################
start_time_overall = time.time()

################### case 1 ###################

print("############################case 1############################")

nb_elem_base = int(input("Entrez le nombre de projets à créer depuis les données scarpper [1-200](nb_elem): ") or "1")


# Load projects from CSV
df_projects = pd.read_csv("../../../data/data_scrapped/ikea_foundation_projects.csv")

# Process each project
results = []
start_time = time.time()

for index, row in df_projects.head(nb_elem_base).iterrows():
    print("generation of data for the project number ", index + 1)
    project_info = row.to_json()
    prompt_template = create_template(1, project_info,"previous_part","general_info", "template_part")
    filled_info = get_response(prompt_template)
    filled_infoo = create_dict_from_text(
        filled_info, row.Description
    )  # on crée un dictionnaire avec les données générées et on ajoute la description
    results.append(filled_infoo)

end_time = time.time()
execution_time = end_time - start_time


# Create a DataFrame from the results
df_results = pd.DataFrame(results)

# Save the filled DataFrame to a new CSV file
df_results.to_csv("../../../data/data_gen/filled_projects.csv", index=False)

print(f"Execution time case 1 with {nb_elem_base} projets: {execution_time:.2f} seconds")


################### case 2 ###################
print("############################case 2############################")

# Demander à l'utilisateur le nombre de projets à créer
nb_elem = min(int(input("Entrez le nombre de projets à créer [1,nb_elem] : ")or 1),nb_elem_base)

# Load projects from CSV
df_projects = pd.read_csv("../../../data/data_gen/filled_projects.csv")

# Process each project
results = []
start_time = time.time()

for index, row in df_projects.head(nb_elem).iterrows():
    print("generation of the project number ", index + 1)
    project_data = row.to_json()
    prompt = create_template(2, project_data,"previous_part", "general_info", "template_part")
    filled_info = get_response(prompt)
    results.append(filled_info)

end_time = time.time()
execution_time = end_time - start_time


# Create a DataFrame from the results
df_results = pd.DataFrame(results, columns=["Filled Project Report"])

# Save the filled DataFrame to a new CSV file
df_results.to_csv("../../../data/data_gen/projects_report.csv", index=False)

print(f"Execution time case 2 with {nb_elem} projet: {execution_time:.2f} seconds")


################### case 3 ###################

print("############################case 3############################")


df_general_info = pd.read_csv("../../../data/data_scrapped/yearly_report_data.csv")
df_projects_report = pd.read_csv("../../../data/data_gen/projects_report.csv")
df_annal_template = pd.read_csv("../../../data/data_scrapped/annualrewiew_template.csv")


# get the data of the riht form:
#yearly_report_ikea = df_yearly_report.to_string(index=False)
project_info = df_projects_report.to_string(index=False)
general_info = df_general_info.to_string(index=False)


start_time = time.time()
yearly_parts = []
for index, part in df_annal_template.iterrows():
    case_0 = "this is the first part we are creating hence no previous part"
    print("Generating yearly report parts",index+1)
    if index == 0:
        prompt = create_template(3, project_info,case_0, general_info, part["contenu"])
    else:
        prompt = create_template(3, project_info,yearly_parts[index-1], general_info, part["contenu"])
    response = get_response(prompt)
    yearly_parts.append(response)

# Create a new DataFrame to store the report parts
df_yearly_report = pd.DataFrame({"partie": df_annal_template.index +1, "contenu": yearly_parts})

# Save the report parts to a new CSV file
output_file = "../../../data/data_gen/yearly_by_part.csv"
df_yearly_report.to_csv(output_file, index=False)
execution_time = time.time() - start_time

print(f"Execution time case 3: {execution_time:.2f} seconds")

##################################################################################

df_yearly_report = pd.read_csv("../../../data/data_gen/yearly_by_part.csv")
start_time = time.time()
combined_string = ' '.join(df_yearly_report['contenu'])

prompt= f"""Task: Transform a Yearly Report into a Continuous Narrative

            Input Text, the yearly report writen by part:{combined_string}

            Objective: Rewrite the provided text into a cohesive, continuous document. Avoid redundancy and ensure smooth transitions between sections.

            Instructions:

            1. Eliminate Redundancies: Identify and remove repeated information.
            2. Ensure Smooth Transitions: Link sections seamlessly without summarizing at transitions. you can put a tiltle for each section as you will have in the writen by part version.
            3. Maintain Professional Tone: Keep the tone formal and suitable for stakeholders.
            4. Review for Flow and Accuracy: Ensure the narrative flows logically and retains all factual data accurately.

            Your rewrite should create a streamlined, logically coherent report that communicates effectively without unnecessary repetition.

            attention there is 12 part in the yearly report and i want all of them in th efinal results. hence you should have 12 subtitles titles in the final results. here are the different part: 
        

            The final result should be a continuous narrative that flows logically from one section to the next anf must be appriximately the same length as the input text.
            the final result must be composed of 12 subtitles titles. for each part of the yearly report, the context and info are in the Input Text. Here are the name of the different part.
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
            """
reponse = get_response(prompt)

# Chemin du fichier CSV
output_file = "../../../data/data_gen/yearly_final.csv"

# Écriture dans le fichier CSV
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Écrire la chaîne dans une ligne du CSV
    writer.writerow([reponse])



execution_time = time.time() - start_time

print(f"Execution time cleaning yealy report: {execution_time:.2f} seconds")

end_time_overall = time.time()
execution_time_overall = end_time_overall - start_time_overall
print(f"Execution time overall: {execution_time_overall:.2f} seconds")

print("############################End of the generation############################")

##################################################################################
