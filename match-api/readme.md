# Melody-Match backend service

## Features:
1. Song indexing (currently only supports track titles)
2. Query by song title (with limiting)

## Set up
1. Set up venv `python -m venv venv` and activate `source venv/Scripts/activate`
2. Install dependencies `pip install -r requirements.txt`
3. Start dev server `flask run --host=0.0.0.0 --debug`

## Deployment

## Dev instructions
- Reasonably comment code 
- Update `readme.md` in a timely manner
- Commit regularly
- When introducing new dependencies, make sure to extend requirements: `pip freeze > requirements.txt`
