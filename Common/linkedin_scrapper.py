# Common/linkedin_scrapper.py

import requests
from urllib.parse import urlparse

API_KEY = "67e57b5f927d1ae6614de520"

def scrape_linkedin_profile(linkedin_url: str):
    linkedin_url = linkedin_url.strip()
    print(f"[INFO] Scraping LinkedIn URL: {linkedin_url}")

    if not linkedin_url.startswith("http"):
        linkedin_url = "https://" + linkedin_url
        print(f"[DEBUG] Normalized URL: {linkedin_url}")

    parsed = urlparse(linkedin_url)
    path_parts = parsed.path.strip("/").split("/")
    print(f"[DEBUG] Parsed Path Parts: {path_parts}")

    if len(path_parts) < 2 or path_parts[0] != "in":
        print("[WARN] Not a valid LinkedIn profile URL (person). Skipping.")
        return {"status": "skipped", "reason": "Not a person profile", "url": linkedin_url}

    slug = path_parts[1]
    print(f"[INFO] Extracted Slug: {slug}")

    api_url = "https://api.scrapingdog.com/linkedin"
    params = {
        "api_key": API_KEY,
        "type": "profile",
        "linkId": slug,
        "private": "false"
    }

    print(f"[DEBUG] Making API call to: {api_url}")
    print(f"[DEBUG] With params: {params}")

    try:
        response = requests.get(api_url, params=params)
        print(f"[INFO] API Response Status: {response.status_code}")

        if response.status_code == 200:
            print("[SUCCESS] Successfully scraped LinkedIn profile.")
            return {"status": "success", "data": response.json()}
        else:
            print(f"[ERROR] Failed to scrape profile. Message: {response.text}")
            return {
                "status": "error",
                "code": response.status_code,
                "message": response.text
            }
    except Exception as e:
        print(f"[EXCEPTION] An error occurred: {e}")
        return {"status": "error", "message": str(e)}
