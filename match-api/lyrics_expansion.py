'''
Use fasttext to expand the query with similar words from the lyrics BOW. Return a set with the tokens and it similar words
Info: https://fasttext.cc/docs/en/crawl-vectors.html

To install fasttext & the english model, run the following commands:
!pip install fasttext
fasttext.util.download_model('en', if_exists='ignore')  # English

'''
import numpy as np
import pickle
import fasttext
import fasttext.util
from utils.text_processing import normalize, process_text, remove_stopwords, tokenize_text

def load_precomputed_similar_words(path):
    with open(path, 'rb') as file:
        return pickle.load(file)

def get_word_vectors(words, ft):
    '''Get the word vectors for a list of words using fasttext, and normalize them for cosine similarity.'''

    # Compute vector matrix for lyrics words
    word_vectors = np.array([ft.get_word_vector(word) for word in words]).astype('float32')

    # Normalize vectors for cosine similarity
    word_norms = np.linalg.norm(word_vectors, axis=1, keepdims=True)
    word_norms[word_norms == 0] = 1  # Avoid division by zero
    word_vectors /= word_norms  # Normalize all vectors

    return word_vectors

def fasttext_exact_nn(word, lyrics_vectors, lyrics_word_map, ft, k, threshold):
    """
    Finds the most similar words using exact cosine similarity through fasttext vectors
    Returns a dictionary of the most similar stemmed words

    Args:
        word: Query word.
        lyrics_words: List of all lyrics words.
        lyrics_vectors: Precomputed matrix of lyrics word vectors.
        lyrics_word_map: Mapping from index to lyrics word.
        ft: FastText model.
        k: Number of nearest neighbors to retrieve.
        threshold: Minimum similarity score.

    Returns:
        Set of similar words that meet the threshold.
    """
    word_vector = np.array(ft.get_word_vector(word)).astype('float32')

    # Normalize input vector
    word_norm = np.linalg.norm(word_vector)
    if word_norm == 0:
        return set()  # Avoid division by zero

    word_vector /= word_norm  # Normalize query vector

    # Compute exact cosine similarity with all lyrics words
    similarities = np.dot(lyrics_vectors, word_vector)

    # Get top-k similar words
    top_indices = np.argsort(similarities)[::-1][:k]  # Sort descending, take top-k
    similar_words = {lyrics_word_map[i] for i in top_indices if similarities[i] > threshold}

    return similar_words

def expand_query(query: str, ft, precomputed_similar_words, lyrics_vectors, lyrics_word_map, lyrics_5000_stems, threshold=0.8, k=20):
    """
    Expands a query by using precomputed similar words when available, 
    and falling back to exact cosine similarity for unseen words.
    """
    # Tokenize, remove stopwords, and get unique words
    words = remove_stopwords(tokenize_text(query))
    stems = normalize(words)

    extended_tokens = []

    for word, stem in zip(words, stems):
        if word in precomputed_similar_words:
            similar_words = precomputed_similar_words[word]  # Use precomputed values
        else:
            similar_words = fasttext_exact_nn(word, lyrics_vectors, lyrics_word_map, ft, k=k, threshold=threshold)
        
        # Stem & remove duplicated words
        similar_stems = set(normalize(similar_words)) | {stem}
        # Add to the query only if the stem is in the 5000 top-stems
        extended_tokens.extend([stem for stem in similar_stems if stem in lyrics_5000_stems])
        
        # Ensure similar_words does not contain the word
        similar_words.discard(word)

    return extended_tokens

if __name__ == '__main__':

    # Paths
    lyrics_precomputed_similar_path = 'data/stored_data/precomputed_similar_stems_lyrics.pkl'
    lyrics_5000_stems_path = 'data/stored_data/lyrics_5000_stems.txt'

    # Load the fasttext model
    ft = fasttext.load_model('models/cc.en.300.bin')

    # Load the 5000 lyrics stems
    with open(lyrics_5000_stems_path, 'r') as file:
        lyrics_5000_stems = {stem.strip() for stem in file.readlines()}

    # Load precomputed similar words
    precomputed_similar_words = load_precomputed_similar_words(lyrics_precomputed_similar_path)

    # Get the word vectors for the lyrics words
    lyrics_words = list(precomputed_similar_words.keys())
    lyrics_vectors = get_word_vectors(lyrics_words, ft)
    lyrics_word_map = {i: word for i, word in enumerate(lyrics_words)}

    query='I love cats in cute hats'
    expanded_query = expand_query(query, ft, precomputed_similar_words, lyrics_vectors, lyrics_word_map, lyrics_5000_stems)
    print(query, "->", expanded_query)