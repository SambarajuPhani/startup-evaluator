from crewai import Agent, Task
import pandas as pd
import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import DocumentAnalysisFeature, AnalyzeResult

load_dotenv()

endpoint = os.getenv("AZURE_DOC_INTEL_END_POINT")
key = os.getenv("AZURE_DOC_INTEL_KEY")

# Define the Data Extraction Agent
data_extractor_agent = Agent(
    role="Data Extraction Agent",
    goal="Extract and format all relevant data from pdf or ppt",
    backstory="Expert at parsing pdf and ppt documents and structuring them into clean readable text.",
)

# Define the task function that returns structured JSON-like result
def get_pitch_deck_task(linkedin_url: str, website_url: str, pitch_path: str) -> Task:
    def extract_and_format_document(file_path: str) -> dict:
        document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

        with open(file_path, "rb") as file:
            file_content = file.read()

        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-read",
            file_content,
            features=[DocumentAnalysisFeature.LANGUAGES]
        )

        result: AnalyzeResult = poller.result()
        formatted_text = result.content

        return {
            "data": formatted_text,
            "linkedin_url": linkedin_url,
            "website_url": website_url,
            "pitch_path": pitch_path
        }

    file_path = "8.pdf"
    structured_result = extract_and_format_document(file_path)

    return Task(
        description="Extract and format data from pdf or ppt. Output as structured JSON with keys: 'data', 'linkedin_url', 'website_url', 'pitch_path'.",
        expected_output=structured_result,
        agent=data_extractor_agent
    )
