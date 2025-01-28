# Melody-Match backend service

## Features:
1. Song indexing (currently only supports track titles)
2. Query by song title (with limiting)

## Set up back-end
1. Set up venv `python -m venv venv` and activate `source venv/Scripts/activate`
2. Install dependencies `pip install -r requirements.txt`
3. Start dev server `flask run --host=0.0.0.0 --debug`

# Set up front-end
4. Install dependencies `npm i`
5. Launch front-end server `npm run dev`

## Deployment

## Dev instructions
- Reasonably comment code 
- Update `readme.md` in a timely manner
- Commit regularly
- When introducing new dependencies, make sure to extend requirements: `pip freeze > requirements.txt`
