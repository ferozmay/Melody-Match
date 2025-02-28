'''
Use fasttext to expand the query with similar words from the lyrics BOW.
Info: https://fasttext.cc/docs/en/crawl-vectors.html

To install fasttext & the english model, run the following commands:
!pip install fasttext
fasttext.util.download_model('en', if_exists='ignore')  # English
'''
import pickle
import fasttext
import fasttext.util
from utils.text_processing import normalize, process_text

# def load_lyrics_inverted_index(path='data/lyrics_inverted_idx.pkl'):
#     '''load the lyrics_inverted_index from a pickle file'''
#     with open(path, 'rb') as file:
#         lyrics_inverted_index = pickle.load(file)
#     print(f"lyrics_inverted_index loaded from pickle at {path}")
#     return lyrics_inverted_index

def load_lyrics_similarity_dict(path='data/lyrics_similarity_dict.pkl'):
    '''load the lyrics_similarity_dict from a pickle file'''
    with open(path, 'rb') as file:
        lyrics_similarity_dict = pickle.load(file)
    print(f"lyrics_similarity_dict loaded from pickle at {path}")
    return lyrics_similarity_dict

def load_expansion_model_dicts(ft_path, lyrics_similarity_dict_path, lyrics_inverted_index_path):
    # Load word2vec model
    ft = fasttext.load_model(ft_path)
    print("fasttext model loaded")

    # Load similar words dictionary
    lyrics_similarity_dict = load_lyrics_similarity_dict(lyrics_similarity_dict_path)

    return ft, lyrics_similarity_dict

def expand_query(query, lyrics_similarity_dict: dict, embeddings, verbose=False):
    '''
    Given a query, expand it with similar tokens from the lyrics BOW.

    First, check if the word is alrady in the lyrics_similarity_dict.
    Otherwise, get the embeddings from fasttext and get the similar words
    '''

    # Convert query into a set of stemmed tokens
    tokens = set(process_text(query).split())
    
    # Check for tokens not present in the lyrics
    tokens_in_lyrics = tokens & set(lyrics_similarity_dict.keys())
    unseen_tokens = tokens - tokens_in_lyrics

    # Expand with seen tokens
    expanded_tokens = tokens_in_lyrics
    expanded_tokens |= {similar_token for token in tokens_in_lyrics for similar_token in lyrics_similarity_dict[token]}

    # Expand with unseen tokens (if present)
    if unseen_tokens:
        for token in unseen_tokens:
            # Get similar words for unseen tokens
            similar_words = {word.lower() for score, word in embeddings.get_nearest_neighbors(token, k=20) if score > 0.7}

            # Normalize the words
            similar_tokens = {token for token in normalize(similar_words) if token in lyrics_similarity_dict.keys()}

            # Add the similar tokens to the set of tokens
            expanded_tokens |= similar_tokens

    if verbose:
        print('Original tokens:', tokens)
        print('Tokens not in lyrics:', unseen_tokens)
    
    # Return the expanded query
    return expanded_tokens

if __name__ == '__main__':

    # Load all required models and dicts
    ft, lyrics_similarity_dict = load_expansion_model_dicts('cc.en.300.bin', 'data/lyrics_similarity_dict.pkl')

    # Example query
    query = 'reew ewre love'
    expanded_tokens = expand_query(query, lyrics_similarity_dict, ft, verbose=True)
    print(query, '->', expanded_tokens)