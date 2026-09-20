import hashlib, json
from pathlib import Path
import feedparser

def load_sources(path):
    p=Path(path)
    return json.loads(p.read_text()).get("sources", []) if p.exists() else []

def fetch_rss(source):
    parsed=feedparser.parse(source["url"])
    out=[]
    for item in parsed.entries:
        raw=item.get("id") or item.get("link") or item.get("title","")
        out.append({
            "source": source["name"],
            "external_id": hashlib.sha256(raw.encode()).hexdigest(),
            "title": item.get("title","").strip(),
            "company": item.get("author","") or source["name"],
            "location": item.get("location",""),
            "url": item.get("link",""),
            "description": item.get("summary","")
        })
    return out
