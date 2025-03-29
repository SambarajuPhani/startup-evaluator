from langgraph.graph import StateGraph, END
from crewai import Agent, Task, Crew
import pandas as pd
from typing import TypedDict, Optional

from Agents.data_extractor_agent import get_data_extraction_task
from Agents.linkedin_agent import get_linkedin_scraping_task  
from Agents.pitch_deck_agent import get_pitch_deck_task


# --- Step 0: Define state schema using TypedDict ---
class AgentState(TypedDict):
    data_path: str
    linkedin_url: str
    website_url: str
    pitch_path: str
    extracted_data: Optional[dict]  # Output from DataExtractionAgent
    linkedin_data: Optional[dict]
  


# --- Step 1a: Data Extraction Node ---
def run_data_extraction_agent(state: AgentState) -> AgentState:
    data_path = state.get("data_path", "")
    print("[RUNNING] Data Extraction Agent with file:", data_path)
    task = get_data_extraction_task(data_path)
    output = task.expected_output  # Assuming pre-executed
    return {
        **state,
        "extracted_data": output
    }


# --- Step 1b: LinkedIn Scraper Node ---
def run_linkedin_scraper_agent(state: AgentState) -> AgentState:
    linkedin_url = state.get("linkedin_url", "")
    print("[RUNNING] LinkedIn Scraper Agent with URL:", linkedin_url)

    task = get_linkedin_scraping_task(linkedin_url)
    crew = Crew(tasks=[task])
    result = crew.run()

    return {
        **state,
        "linkedin_data": result
    }


# --- Step 2: Build LangGraph ---
builder = StateGraph(AgentState)

builder.add_node("DataExtractionAgent", run_data_extraction_agent)
builder.add_node("LinkedInScraperAgent", run_linkedin_scraper_agent)  # ✅ Add LinkedIn node

# Define graph flow
builder.set_entry_point("DataExtractionAgent")
builder.add_edge("DataExtractionAgent", "LinkedInScraperAgent")
builder.set_finish_point("LinkedInScraperAgent")

graph = builder.compile()

# --- Step 3: Run the graph ---
input_state = {
    "data_path": "sample_data.xlsx",
    "linkedin_url": "https://www.linkedin.com/in/sachit-upadhyay/",
    "website_url": "",
    "pitch_path": "",
    "extracted_data": None,
    "linkedin_data": None
}

final_output = graph.invoke(input_state)

# Print full JSON output
import json
print(json.dumps(final_output, indent=2))
