# README: Medical Data Extraction Pipeline

## Overview

A comprehensive solution that integrates Azure Machine Learning Services (LLMS) to analyze and process healthcare data. This pipeline is specifically designed for the competition hosted on Azure. The main components include data preprocessing, translation, interaction with a scoring service, and storage of results in Azure Blob Storage.

## Code Structure

### Transcription and Translation

- The code begins by loading patient transcripts from the provided `input_1.json` file.
- Utilizes the Googletrans library for translation, ensuring that the data is in English for further processing.

### Azure ML Scoring Service Integration

- The pipeline leverages Azure Machine Learning Services (LLMS) to interact with a scoring service deployed at `https://roberta.eastus.inference.ml.azure.com/score`.
- A set of predefined questions related to patient information is used to query the service for answers.
- The obtained scores and answers are then collected for analysis.

### Data Processing

- The results are organized into a structured format, creating a DataFrame that includes information such as Transcript ID, Question, Answer, and Scores.
- This DataFrame is saved as a CSV file named `input_1.csv`.

### Azure Blob Storage

- The pipeline utilizes Azure Blob Storage for storing the processed data.
- A connection string and container information are configured to upload the CSV file to Azure Blob Storage.

## Azure Pipeline

- The pipeline showcases the integration of various Azure services for end-to-end data processing.
- Data is translated, sent to a scoring service, and the results are stored in Azure Blob Storage for easy access.

## How to Run

1. **Install Dependencies:**
   - Ensure that all required dependencies, including Azure ML SDK, Googletrans, and Pandas, are installed. Use the following command:
     ```bash
     pip install azureml-sdk googletrans==4.0.0-rc1 pandas
     ```

2. **Azure ML Authentication:**
   - Make sure to set up your Azure Machine Learning authentication by configuring your Azure ML workspace. Refer to the [Azure ML SDK documentation](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-manage-workspace).

3. **Run the Code:**
   - Execute the provided Python script (`competition_pipeline.py`) to run the competition pipeline.

4. **Review Results:**
   - Check the output CSV file (`input_1.csv`) to see the results of the scoring service for each transcript and question.

## Azure Pipeline Configuration

- The Azure Pipeline is not explicitly provided in this code snippet. However, the pipeline can be configured on Azure DevOps or any CI/CD platform to automate the execution of the provided script.

## Note

- Ensure that you have the necessary permissions and configurations in your Azure environment to use Azure ML services and Azure Blob Storage.


