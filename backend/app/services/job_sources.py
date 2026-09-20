import os
import httpx
import feedparser

def fetch_adzuna(source):
    """
    Adzuna REST API adapter.
    Required env vars: ADZUNA_APP_ID, ADZUNA_APP_KEY.
    source fields: country, query, where, page.
    """
    app_id = os.getenv("ADZUNA_APP_ID", "")
    app_key = os.getenv("ADZUNA_APP_KEY", "")
    if not app_id or not app_key:
        return []
    country = source.get("country", "in")
    page = source.get("page", 1)
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "results_per_page": source.get("results_per_page", 50),
        "what": source.get("query", "software engineer"),
        "where": source.get("where", "India"),
        "content-type": "application/json",
    }
    url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}"
    r = httpx.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    jobs = []
    for item in data.get("results", []):
        jobs.append({
            "source": source["name"],
            "external_id": str(item.get("id") or item.get("redirect_url")),
            "title": item.get("title", ""),
            "company": (item.get("company") or {}).get("display_name", ""),
            "location": (item.get("location") or {}).get("display_name", ""),
            "url": item.get("redirect_url", ""),
            "description": item.get("description", ""),
        })
    return jobs

def fetch_lever_public(source):
    """
    Lever public XML feed adapter.
    source field: company_slug.
    Use only for companies whose public Lever feed is intended for job-board use.
    """
    slug = source["company_slug"]
    url = f"https://api.lever.co/v0/postings/{slug}?mode=xml"
    r = httpx.get(url, timeout=30)
    r.raise_for_status()
    parsed = feedparser.parse(r.text)
    jobs = []
    for item in parsed.entries:
        jobs.append({
            "source": source["name"],
            "external_id": str(item.get("id") or item.get("link")),
            "title": item.get("position") or item.get("title", ""),
            "company": source.get("company_name", slug),
            "location": item.get("location", ""),
            "url": item.get("apply_url") or item.get("link", ""),
            "description": item.get("description", ""),
        })
    return jobs
