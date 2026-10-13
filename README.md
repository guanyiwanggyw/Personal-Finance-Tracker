# Personal Finance Tracker

A personal finance tracker intended to sync bank transactions and provide a
clear view of spending across accounts. The project is at an early prototype
stage: the Django backend is scaffolded, and Monzo access and data export are
being explored.

## Checkpoint 14/10/2026 00:47

### In place

- Django project configuration with Django REST Framework installed.
- `accounts` and `transactions` Django app scaffolds.
- Scratch scripts for Monzo OAuth, token refresh, API probing, and data export.
- The backfill fetches accounts, balances, pots, and transactions in 30-day
  windows, saving JSON under `backend/scratch/raw/`.
- Local environment files, the SQLite database, and scratch data are excluded
  from Git.

### Planned stack and progress

| Area      | Plan                  | Progress                                           |
| --------- | --------------------- | -------------------------------------------------- |
| Frontend  | React                 | Not started                                        |
| Backend   | Django REST Framework | Scaffolded; no finance models or API endpoints yet |
| Database  | PostgreSQL            | Planned; currently configured for local SQLite     |
| Bank data | Monzo API             | OAuth and JSON backfill experiments underway       |

**Overall:** early prototype; there is not yet a complete frontend-to-database
flow.

### Next steps

- [ ] Verify the Monzo login, token refresh, and backfill flow; note any API
      limits.
- [ ] Create account and transaction models, migrations, and PostgreSQL
      configuration.
- [ ] Import and de-duplicate the exported JSON.
- [ ] Add tested API endpoints, then build the React frontend and spending
      summaries.

## Project layout

```text
backend/
├── accounts/       # Django app scaffold
├── config/         # Django settings and URL configuration
├── scratch/        # Local Monzo experiments and generated data (gitignored)
│   ├── monzo_auth.py    # Sign in to Monzo and save access tokens
│   ├── monzo_common.py  # Shared API settings and token refresh helpers
│   └── backfill.py      # Fetch account data and save it as JSON
├── transactions/   # Django app scaffold
├── manage.py
├── requirements.txt
└── .env.example
```

## Local setup

The commands below use PowerShell and assume Python is installed. From the
repository root:

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
Copy-Item .env.example .env
pip install -r requirements.txt
```

Set `DJANGO_SECRET_KEY` in `.env` to a private value and use `DEBUG=True` only
for local development. To use the Monzo scripts, also set the client ID,
client secret, and redirect URI to match your Monzo application.

Run Django from `backend/`:

```powershell
py manage.py migrate
py manage.py runserver
```

The only configured application route is Django admin at
`http://127.0.0.1:8000/admin/`.

## Monzo scratch workflow

These scripts are exploratory, local-only tooling, not a production banking
integration:

- `monzo_auth.py` opens the Monzo sign-in flow, receives the callback, and
  saves the tokens after you approve access.
- `monzo_common.py` provides shared Monzo configuration and functions used
  by the other scripts to load and refresh those tokens.
- `backfill.py` uses the tokens to request account details and transactions,
  then saves the responses as JSON in 30-day windows.

From `backend/`, run `python scratch/monzo_auth.py`. After access is approved
in the Monzo app, it saves the tokens and starts `backfill.py`.

The backfill saves raw data under `backend/scratch/raw/`. Treat that directory
and `backend/scratch/tokens.json` as sensitive; do not commit or share them.
The scratch scripts require `requests`, which is not currently listed in
`backend/requirements.txt`.
