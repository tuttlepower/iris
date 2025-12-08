# Iris URL Redirector

A minimal FastAPI service that rewrites any HTTP/HTTPS URL to common archive, reader, and raw views. The root route provides a tiny Bootstrap page for quick redirects.

## Routes
- `GET /` – Bootstrap landing page with URL input and buttons.
- `GET /a/{url}` – 302 redirect to `archive.ph`.
- `GET /w/{url}` – 302 redirect to the Wayback Machine.
- `GET /12/{url}` – 302 redirect to `12ft.io`.
- `GET /r/{url}` – 302 redirect to a lightweight reader view.
- `GET /raw/{url}` – Fetches the raw HTML (up to 1 MB) with timeouts and returns it directly.

Private, loopback, and link-local addresses are blocked. Invalid requests return clean HTML error pages for 400, 403, 404, and 504 scenarios.

## Local Development
Install dependencies and run the FastAPI app with Uvicorn:

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Open http://localhost:8000 to use the landing page.

## Deployment
The included `vercel.json` builds the FastAPI app via `@vercel/python` and routes all traffic to `main.py` for serverless hosting on Vercel.
