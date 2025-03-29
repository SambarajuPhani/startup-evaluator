# test_linkedin_task.py

from crewai import Crew
from Agents.linkedin_agent import get_linkedin_scraping_task

if __name__ == "__main__":
    task = get_linkedin_scraping_task("https://www.linkedin.com/in/sachit-upadhyay/")
    crew = Crew(tasks=[task])

    result = crew.run()

    import json
    print(json.dumps(result, indent=2))
