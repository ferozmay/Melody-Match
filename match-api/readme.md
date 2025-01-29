# Melody-Match backend service

## Features:
1. Song indexing (currently only supports track titles)
2. Query by song title (with limiting)

## Set up back-end
0. The following commands are to be run from within the `Melody-Match/match-api/` directory 
1. Set up venv `python -m venv venv`
2. Activate venv with `source venv/Scripts/activate` or `source venv/bin/activate` depending on OS
3. Install dependencies `pip install -r requirements.txt`
4. Run `python -m index.clean_store_load`
5. Start dev server `flask run --host=0.0.0.0 --debug`

# Set up front-end
1. Install dependencies `npm i`
2. Launch front-end server `npm run dev`

## Deployment

## Dev instructions
- Reasonably comment code 
- Update `readme.md` in a timely manner
- Commit regularly
- When introducing new dependencies, make sure to extend requirements: `pip freeze > requirements.txt`
