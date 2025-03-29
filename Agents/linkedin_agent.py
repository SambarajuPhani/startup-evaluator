# linkedin_scraper_agent.py

import requests
from urllib.parse import urlparse
from crewai import Agent, Task, Crew

# --- LinkedIn Scraper Function ---
API_KEY = "67e57b5f927d1ae6614de520"

def scrape_linkedin_profile(linkedin_url: str):
    linkedin_url = linkedin_url.strip()
    print(f"[INFO] Scraping LinkedIn URL: {linkedin_url}")

    if not linkedin_url.startswith("http"):
        linkedin_url = "https://" + linkedin_url

    parsed = urlparse(linkedin_url)
    path_parts = parsed.path.strip("/").split("/")

    if len(path_parts) < 2 or path_parts[0] != "in":
        return {"status": "skipped", "reason": "Not a person profile", "url": linkedin_url}

    slug = path_parts[1]
    api_url = "https://api.scrapingdog.com/linkedin"
    params = {
        "api_key": API_KEY,
        "type": "profile",
        "linkId": slug,
        "private": "false"
    }

    try:
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            return {"status": "success", "data": response.json()}
        else:
            return {
                "status": "error",
                "code": response.status_code,
                "message": response.text
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# --- Create Agent WITHOUT tools ---
linkedin_scraper_agent = Agent(
    role="LinkedIn Scraper",
    goal="Extract structured JSON data from a LinkedIn profile.",
    backstory="Expert at pulling data from LinkedIn using APIs.",
    verbose=True
)

# --- Embed logic directly inside the Task function ---
def get_linkedin_scraping_task(linkedin_url: str) -> Task:
    def execute_scraping() -> str:
        result = scrape_linkedin_profile(linkedin_url)
        return str(result)

    return Task(
        description=f"Scrape LinkedIn profile: {linkedin_url}",
        agent=linkedin_scraper_agent,
        expected_output="Structured JSON with profile details.",
        async_execution=False,
        context=[],
        steps=[execute_scraping]  # ✅ embed logic directly
    )

# --- Run ---
if __name__ == "__main__":
    task = get_linkedin_scraping_task("https://www.linkedin.com/in/sachit-upadhyay/")
    crew = Crew(agents=[linkedin_scraper_agent], tasks=[task], verbose=True)
    result = crew.kickoff()
    print("\n=== FINAL OUTPUT ===\n")
    print(result)
