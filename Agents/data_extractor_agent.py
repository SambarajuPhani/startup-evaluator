from crewai import Agent, Task
import pandas as pd
import json

# Define the Data Extraction Agent
data_extractor_agent = Agent(
    role="Data Extraction Agent",
    goal="Extract and format all relevant data from Excel",
    backstory="Expert at parsing Excel spreadsheets and structuring them into clean readable text.",
)

# Define the task function that returns structured JSON-like result
def get_data_extraction_task(data_path: str) -> Task:
    def extract_and_format_excel(data_path: str) -> dict:
        df = pd.read_excel(data_path)
        df = df.fillna("Data not available")
        df = df.replace(r'^\\s*$', "Data not available", regex=True)

        text_chunks = []
        for _, row in df.iterrows():
            row_text = "\\n".join(f"{col}: {row[col]}" for col in df.columns)
            text_chunks.append(row_text)

        formatted_text = "\\n\\n".join(text_chunks)

        return {
            "data": formatted_text
        }

    structured_result = extract_and_format_excel(data_path)

    return Task(
        description="Extract and format data from Excel. Output as structured text",
        expected_output=json.dumps(structured_result),
        agent=data_extractor_agent
    )
