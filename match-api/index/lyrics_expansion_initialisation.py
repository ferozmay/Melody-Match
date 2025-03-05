'''
Functions to create the inversed index for the lyrics dataset,
And to create a dictionary with similar words for all 5000 words in lyrics

Lyrics in BOW format can be downloaded from here:
train_file: http://millionsongdataset.com/sites/default/files/AdditionalFiles/mxm_dataset_train.txt.zip
test_file: http://millionsongdataset.com/sites/default/files/AdditionalFiles/mxm_dataset_test.txt.zip

Run from the command line (from match-api/ folder):
python -m match-api.index.lyrics_expansion_initialisation

'''
from utils.text_processing import normalize
import fasttext
import fasttext.util
import pickle
import re
import numpy as np

### create index - related functions
def read_lyrics(lyrics_train_path, lyrics_test_path):
    '''
    Combine the lyrics from the train and test files into a dictionary
    Returns: a dictionary with the format {'word_idx': {'track_id': counts}} 
    '''
    lyrics_dict = {}

    # Read the lyrics from the train and test files
    for lyrics_path in [lyrics_train_path, lyrics_test_path]:
        with open(lyrics_path, 'r') as file:
            for line in file:
                if line.startswith('#'):
                    continue # It is a comment
                if line.startswith('%'):
                    # List of all words
                    lyrics_5000_stems = line[1:].split(',')
                elif line.startswith('TR'):
                    line = line.split(',')
                    track_id = line[0]
                    word_dict = {int(id): int(freq) for id_freq in line[2:] for id, freq in [id_freq.split(':')]}
                    lyrics_dict[track_id] = word_dict

    return lyrics_dict, lyrics_5000_stems

def make_inverted_index(lyrics_word_dict: dict, all_words: list) -> dict:
    '''
    Input: {track_id: {word: count}}
    Output: {word: {track_id: count}}
    '''
    # Initialize an empty list for each word in the vocabulary
    inverted_index = {word: {} for word in all_words}
    
    # Iterate over each track and its corresponding word dictionary
    for track_id, word_dict in lyrics_word_dict.items():
        # Iterate over each word ID in the word dictionary
        for word, count in word_dict.items():
            # Get the word corresponding to the word ID and append the track ID
            inverted_index[word][track_id] = count
    
    return inverted_index

def save_lyrics_inverted_index(lyrics_inverted_index, path='data/stored_data/lyrics_inverted_word.pkl'):
    with open(path, 'wb') as file:
        pickle.dump(lyrics_inverted_index, file)
    print(f"lyrics_inverted_index saved as pickle at {path}")

### fasttext-related functions
def get_ft_lyrics_words_from_(lyrics_stems: set, ft) -> list:
    '''
    The lyrics BOW dataset only provides stems, not words, while fasttext has been trained on words.
    Get a subset of the 2M words in fasttext whose stems are in the lyrics dataset, for precomputing.

    Input:
    - lyrics_stems: 5000 stems from the lyrics BOW
    - ft_words: all words in fasttext, after lowercasing & removing non-alphanumeric characters
    - ft: fasttext model

    Output:
    - lyrics_words: words in fasttext whose stems are in the lyrics_stems set
    '''

    # Get alphanumeric lowercase fs words
    ft_words = list({re.sub(r'[^a-z0-9]', '', word.lower().strip()) for word in ft.get_words() if re.sub(r'[^a-z0-9]', '', word)})

    # Stem all words in fasttext
    stemmed_fs_words = normalize(ft_words)

    # Get words in fs whose stems are in the lyrics_stems set
    lyrics_words = [word for stem, word in zip(stemmed_fs_words, ft_words) if stem in lyrics_stems]

    return lyrics_words

def get_word_vectors(words, ft):
    '''Get the word vectors for a list of words using fasttext, and normalize them for cosine similarity.'''

    # Compute vector matrix for lyrics words
    word_vectors = np.array([ft.get_word_vector(word) for word in words]).astype('float32')

    # Normalize vectors for cosine similarity
    word_norms = np.linalg.norm(word_vectors, axis=1, keepdims=True)
    word_norms[word_norms == 0] = 1  # Avoid division by zero
    word_vectors /= word_norms  # Normalize all vectors

    return word_vectors

def precompute_similar_stems(lyrics_words, lyrics_vectors, k=20, threshold=0.8, save_path=None):
    """
    Precomputes the most similar words within lyrics_words using exact cosine similarity.

    Args:
        lyrics_words: List of all lyrics words.
        lyrics_vectors: Precomputed matrix of lyrics word vectors.
        lyrics_word_map: Mapping from index to lyrics word.
        k: Number of nearest neighbors to retain.
        threshold: Minimum similarity score.

    Returns:
        Dictionary {word: set(similar_words)}
    """
    if save_path:
        assert save_path.endswith('.pkl'), 'Save path must be a .pkl file'

    precomputed_similar_stems = {}

    # Create word index mapping
    lyrics_word_map = {i: word for i, word in enumerate(lyrics_words)}
    word_to_stem = {word: stem for word, stem in zip(lyrics_words, normalize(lyrics_words))}

    # Compute cosine similarity for all pairs
    similarities = np.dot(lyrics_vectors, lyrics_vectors.T)  # Exact similarity (N x N)

    for i, word in enumerate(lyrics_words):
        # Get top-k similar words (excluding itself)
        similar_indices = np.argsort(similarities[i])[::-1][1:k+1]  
        similar_words = {lyrics_word_map[idx] for idx in similar_indices if similarities[i][idx] > threshold}

        # Convert the word into stems
        precomputed_similar_stems[word] = {word_to_stem[word] for word in similar_words}

    if save_path:
        with open(save_path, 'wb') as file:
            pickle.dump(precomputed_similar_stems, file)

    return precomputed_similar_stems


if __name__ == '__main__':

    ## PATHS
    # Input paths
    lyrics_test_path = 'data/msd_metadata/mxm_dataset_test.txt'
    lyrics_train_path = 'data/msd_metadata/mxm_dataset_train.txt'

    # Output
    lyrics_5000_stems_path = 'data/stored_data/lyrics_5000_stems.txt'
    lyrics_inverted_index_path = 'data/stored_data/lyrics_inverted_idx.pkl'
    lyrics_precomputed_similar_path = 'data/stored_data/precomputed_similar_stems_lyrics.pkl'

    # CREATE INVERTED INDEX
    # Load the data
    print("Loading data...")
    lyrics_dict_idx, lyrics_5000_stems = read_lyrics(lyrics_train_path, lyrics_test_path)

    # Make mappings from words to indices, where idx starts at 1
    word_to_idx = {word: index+1 for index, word in enumerate(lyrics_5000_stems)}
    index_to_word = {index+1: word for index, word in enumerate(lyrics_5000_stems)}

    # Create a dictionary with words instead of indices
    lyrics_dict_word = {track_id: {index_to_word[int(id)]: int(freq) for id, freq in word_dict.items()} for track_id, word_dict in lyrics_dict_idx.items()}

    # Make inverted index
    print("Creating inverted index for lyrics dataset...")
    inverted_index = make_inverted_index(lyrics_dict_word, lyrics_5000_stems)

    # Save the inverted index
    save_lyrics_inverted_index(inverted_index)

    # PRECOMPUTE SIMILAR WORDS

    # Load the fasttext model
    print("Loading fasttext model...")
    ft = fasttext.load_model('models/cc.en.300.bin')

    # Get words in fasttext whose stem is in lyrics_stems
    lyrics_ft_words = get_ft_lyrics_words_from_(lyrics_5000_stems, ft)
    lyrics_word_map = {i: word for i, word in enumerate(lyrics_ft_words)}
    print(f"We got {len(lyrics_ft_words)} words in the lyrics from {len(lyrics_5000_stems)} stems")

    # Get the word vectors for the lyrics words
    lyrics_vectors = get_word_vectors(lyrics_ft_words, ft)

    # Run precomputation
    print("Precomputing similar words for lyrics...")
    precomputed_similar_stems = precompute_similar_stems(lyrics_ft_words, lyrics_vectors, save_path=lyrics_precomputed_similar_path)

