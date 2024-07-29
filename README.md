Commitizen

poetry run pre-commit install --hook-type commit-msg

# Getting started

1. You need poetry installed on your machine
2. Clone the repo
3. In `src` change `your_package` to the name of your choice
4. In `pyproject.toml`, at line 7, change `your_package` to the name of your choice
4. Run `poetry install`
5. Run `poetry run doit install_precommit`



## To improve our curent model for tha case of ikea:

- change the retrieval argumets in vectorstore fields[]
- play with the chunk_size=100, chunk_overlap=0 in vector store function CharacterTextSplitter()
- change the answering boat and aswering prompt and other in Answering
- finally you can make changes in .json in the oneGovernace-index. This is for the optinisation of both retrieval and embedings
- in load_document() we can add consideration for json and csv.s
