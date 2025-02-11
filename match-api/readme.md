# Melody-Match backend service

## Features:
1. Song indexing (currently only supports track titles)
2. Query by song title (with limiting)

## Set up back-end
0. The following commands are to be run from within the `Melody-Match/match-api/` directory 
1. Set up venv `python -m venv venv`
2. Activate venv with `source venv/Scripts/activate` or `source venv/bin/activate` depending on OS
3. Install dependencies `pip install -r requirements.txt`
4. Create a folder `data/stored_data/`
4. Run the shell script `./build_index.sh` in the terminal
5. Start dev server `flask run --host=0.0.0.0 --debug`

# Explaining the back-end
0. The modules in the back-end (the `match-api` directory) are executed in the following order, and should probably be read in this order to understand what is happening
1. `index/data_cleaning.py`
2. `index/data_processing.py`
3. `index/inverted_index.py`
4. `index/store_load.py` # this module when executed, runs the main functions of the previous three modules
5. `index/index_class.py`
6. `app.py`
7. `search_rank.py`
8. `utils/ids_to_data.py`


# Set up front-end
1. Install dependencies `npm i`
2. Launch front-end server `npm run dev`
## Deployment

## Dev instructions
- Reasonably comment code 
- Update `readme.md` in a timely manner
- Commit regularly
- When introducing new dependencies, make sure to extend requirements: `pip freeze > requirements.txt`
