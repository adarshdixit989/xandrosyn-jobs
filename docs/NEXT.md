# v10 notification pipeline

Firebase client registration is connected to the backend. The worker now:
1. Reads enabled authorized RSS sources.
2. Deduplicates jobs.
3. Matches jobs against alerts.
4. Creates notification events.
5. Sends FCM messages through Firebase Admin SDK.

Server-side Firebase credentials are intentionally NOT included.

Before running the worker:
- Create a Firebase service account in the Firebase/Google Cloud project.
- Store its JSON securely on the server.
- Set GOOGLE_APPLICATION_CREDENTIALS to its path.
- Do not use the mobile `google-services.json` as server credentials.

Firebase documents recommend the Admin SDK for programmatic FCM sending, and the Flutter client should request notification permission and obtain an FCM token.
