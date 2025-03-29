import os, re
from crewai_tools import ScrapeWebsiteTool, FileWriterTool, TXTSearchTool
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from duckduckgo_search import DDGS
from playwright.sync_api import sync_playwright
import litellm
from bs4 import BeautifulSoup
from typing import Any


class LinkExtractorTool(BaseTool):
    name: str = "Website Link Extractor Tool"
    description: str = "Extracts all links from a given website URL"

    def _run(self, url: str) -> Any:
        try:
            with sync_playwright() as pw:
                browser = pw.chromium.launch(headless=True)
                context = browser.new_context(viewport={"width": 1280, "height": 800})
                page = context.new_page()

                page.goto(url, wait_until="domcontentloaded")

                # page.goto(url, timeout=60000)
                # page.wait_for_load_state("networkidle")
                html = page.content()
                browser.close()

                # Extract all links using BeautifulSoup
                soup = BeautifulSoup(html, "html.parser")
                links = []

                for link in soup.find_all("a", href=True):
                    href = link.get("href")
                    text = link.text.strip()
                    if href and not href.startswith(("#", "javascript:", "mailto:")):
                        # Create a dictionary with both href and link text
                        links.append({"url": href, "text": text if text else "No text"})

                return links
        except Exception as e:
            return f"Error extracting links: {str(e)}"


# Playwright Public Webpage Scraping Tool with Text Extraction
class PlaywrightPublicScrapeTool(BaseTool):
    name: str = "Playwright Public Scrape Tool"
    description: str = (
        "Scrapes public web pages and extracts text content using Playwright."
    )

    def _run(self, url: str) -> Any:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width": 1280, "height": 800})
            page = context.new_page()

            page.goto(url, wait_until="domcontentloaded")
            # page.goto(url, timeout=60000)
            # page.wait_for_load_state("networkidle")

            html = page.content()
            browser.close()

            # Extract text content
            soup = BeautifulSoup(html, "html.parser")

            # Remove form-related content and common CTA phrases
            form_phrases = [
                "fill out this simple form",
                "get back to you ASAP",
                "contact us today",
                "submit your information",
            ]

            # Remove forms
            for form in soup.find_all("form"):
                form.decompose()

            text = soup.get_text(separator=" ", strip=True)

            # Remove form-related phrases
            for phrase in form_phrases:
                text = text.replace(phrase, "")

            # Clean up extra whitespace
            text = " ".join(text.split())

            # Limit text length to reduce token count
            return text[:50000]


# Initialize Tools
link_extractor_tool = LinkExtractorTool()
playwright_tool = PlaywrightPublicScrapeTool()

# scraper_agent = Agent(
#     role="Comprehensive Website Content Extractor",
#     goal="Extract and organize all visible content from every internal page of a given website, producing a structured and readable document.",
#     backstory="An expert web scraper adept at crawling through full websites, extracting clean, readable content from all reachable internal pages and structuring them logically.",
#     tools=[link_extractor_tool, playwright_tool],
#     llm="azure/gpt-4o-mini",
#     verbose=True,
# )

# scrape_task = Task(
#     description=(
#         "For the website {url}, perform the following steps:\n\n"
#         "1. Use playwright_tool to extract and store all the content of the landing page.\n"
#         "2. Use link_extractor_tool to extract all internal links (i.e., links that begin with the same domain or are relative URLs).\n"
#         "3. Filter the links to only include those containing these keywords:\n"
#         "   - contact\n"
#         "   - about\n"
#         "   - services\n"
#         "   - products\n"
#         "   - testimonials\n"
#         "4. For each filtered link using playwright_tool ,extract all content from the page body (avoid hidden, script, or navigation-only content).\n"
#         "5. For each page, structure the content under a clear header indicating the page path or title, e.g.,\n"
#         "   === /about === or === ABOUT US ===\n\n"
#         "6. Ensure:\n"
#         "   - Clear separation between different page sections.\n"
#         "   - All content is human-readable and properly formatted.\n"
#         "   - Repeated elements like navbars/footers are skipped or minimized if possible.\n\n"
#         "7. Combine all page contents into a single, well-structured document."
#     ),
#     agent=scraper_agent,
#     expected_output=(
#         "A single document that includes:\n"
#         "1. Full landing page content under '=== HOME PAGE ==='\n"
#         "2. All other internal pages under headers like '=== /about ===' or '=== CONTACT ==='\n"
#         "3. Deduplicated, well-formatted text with meaningful headers for each section\n"
#         "4. Optional brief page titles if available for easier readability"
#     ),
# )

scraper_agent = Agent(
    role="Website Content Extractor",
    goal="Extract complete text content from website pages while maintaining structure and readability",
    backstory="Specialized web scraping expert focusing on accurate content extraction and organization",
    tools=[link_extractor_tool, playwright_tool],
    llm="azure/gpt-4o-mini",
    verbose=True,
    max_iterations=3,  # Add maximum iterations to prevent infinite loops
)

scrape_task = Task(
    description=(
        "For the website {url}, perform the following steps:\n\n"
        "1. Use playwright_tool to extract and store all the content of the landing page.\n"
        "2. Use link_extractor_tool to extract all internal links (i.e., links that begin with the same domain or are relative URLs).\n"
        "3. Filter the links to only include those containing these keywords:\n"
        "   contact-us\n"
        "   about-us\n"
        "   services\n"
        "   products\n"
        "   testimonials\n"
        "4. For each filtered link using playwright_tool ,extract all content from the page body (avoid hidden, script, or navigation-only content).\n"
        "5. For each page, structure the content under a clear header indicating the page path or title, e.g.,\n"
        "   === /about === or === ABOUT US ===\n\n"
        "6. Ensure:\n"
        "   - Clear separation between different page sections.\n"
        "   - All content is human-readable and properly formatted.\n"
        "   - Repeated elements like navbars/footers are skipped or minimized if possible.\n\n"
        "7. Combine all page contents into a single, well-structured document."
    ),
    agent=scraper_agent,
    expected_output=(
        "Structured document containing:\n"
        "1. Analysis header with metadata\n"
        "2. Landing page content\n"
        "3. Individual sections with headers and URLs\n"
        "4. Clear section separators\n"
        "5. Consistent formatting throughout"
    ),
)

# Initialize crew with the agent and task
crew = Crew(agents=[scraper_agent], tasks=[scrape_task], verbose=True)


if __name__ == "__main__":
    # output = ""
    # keyword_patterns = [
    #     r"contact.*us",
    #     r"testimonial[s]?",
    #     r"about.*us",
    #     r"service[s]?",
    #     r"product[s]?",
    # ]
    # base_url = "https://ecobiotraps.com/"
    # links = link_extractor_tool.run(base_url)
    # print("\n--- Website Links with Keywords ---\n")

    # # Filter links containing keywords
    # filtered_links = set()
    # for link in links:
    #     link_url = link["url"]

    #     # Only process URLs that start with the base URL
    #     if link_url.startswith(base_url):
    #         # Check URL for keyword matches
    #         for pattern in keyword_patterns:
    #             if re.search(pattern, link_url):
    #                 filtered_links.add(link_url)
    #                 break
    # filtered_links = list(filtered_links)

    # if filtered_links:
    #     for link in filtered_links:
    #         # url = link["url"]
    #         # print(f"URL: {url}")
    #         # print(f"Text: {link['text']}")
    #         # print("-" * 50)
    #         print(link)
    #         result = playwright_tool.run(link)
    #         output += "--------------------" + link + "---------------------\n"
    #         output += result
    #         output += "\n"
    #         # print(output)

    # print(output)
    url = "https://ecobiotraps.com/"
    result = crew.kickoff(inputs={"url": url})
    print(result)
