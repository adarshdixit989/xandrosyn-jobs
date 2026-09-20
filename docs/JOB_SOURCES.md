# Real job source plan

## 1. Adzuna
Adzuna provides a REST API for job advertisements. It requires an `app_id` and `app_key`. The adapter in this release supports country, query, location and pagination settings.

Official documentation:
https://developer.adzuna.com/overview

For commercial publishing, review Adzuna's terms and request appropriate limits/access before launch.

## 2. Lever public postings
Lever documents a public Postings API and XML feed for job boards. The adapter accepts a company's Lever slug and reads its public feed.

Official documentation:
https://hire.lever.co/developer/usecases

Only enable a company feed where the public feed is available and its use is permitted.

## 3. More sources
Next adapters can be added for other authorized APIs, feeds, or ATS integrations. Do not scrape protected job boards or bypass access controls.

## Configuration
Enable a source in `backend/sources.json` and set credentials in environment variables. Never commit API keys.
