# Xandrosyn Jobs

**Xandrosyn Jobs** is a job-discovery platform under the **Xandrosyn** software company brand.

This repository contains a production-oriented starter with a Flutter mobile app, FastAPI backend, PostgreSQL-ready persistence, authorized job-source adapters, and Firebase Cloud Messaging notification plumbing.

## Included
- FastAPI backend
- SQLAlchemy models with PostgreSQL-ready configuration
- Authorized job-source adapters for Adzuna and public Lever feeds
- Job deduplication and ingestion worker
- Alert matching and FCM notification pipeline
- Flutter Android client with Firebase Messaging registration
- Environment templates and deployment notes

## Security
- API keys, Firebase service-account credentials, database passwords, and payment secrets are **not** committed.
- The real `google-services.json` should be kept locally and is ignored by Git.
- Copy `mobile/android/app/google-services.json.example` to `google-services.json` and replace the placeholders with your Firebase Android configuration.
- Set production credentials through environment variables / secure deployment secrets.

## Local backend

```bash
cd backend
python -m venv .venv
# Windows PowerShell: .\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Local mobile app

Place your Firebase Android `google-services.json` at:

`mobile/android/app/google-services.json`

Then run the Flutter application from `mobile/`.

## Job sources

See [`docs/JOB_SOURCES.md`](docs/JOB_SOURCES.md) for source configuration and authorization notes.

## Brand architecture

- **Xandrosyn** = software company / master brand
- **Xandrosyn Jobs** = job-platform product
