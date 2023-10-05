# wikidata-bot

## Development

Ensure you have Python 3.6 or higher installed and available as `python`.

To install dependencies:

(with virtual environment - recommended)
1. Run `python -m venv .venv` after cloning the repo
2. `source .venv/bin/activate` (POSIX) or `.venv\Scripts\activate.bat` (Windows CMD) or `.venv\Scripts\Activate.ps1` (Windows PowerShell)
3. `pip install -r requirements.txt`

(without virtual environment - not recommended)
1. Run `pip install -r requirements.txt`

## Run locally against production

`op run --env-file .env.production -- python main.py`

## Run locally against local DB

> [!WARNING]  
> When testing locally, take care to not write any wrong information to Wikidata, as IDs are different between production and seed/local data!

Set up an env file `.env.local` similar to `.env.production` but with the
following changes:

- set `DB_URL` to the URL of your local database
- if there is no authentication, do not set `DB_USER` and `DB_PASSWORD`

Then run: `op run --env-file .env.local -- python main.py`
