'''
Functions to create the inversed index for the lyrics dataset,
And to create a dictionary with similar words for all 5000 words in lyrics

Lyrics in BOW format can be downloaded from here:
train_file: http://millionsongdataset.com/sites/default/files/AdditionalFiles/mxm_dataset_train.txt.zip
test_file: http://millionsongdataset.com/sites/default/files/AdditionalFiles/mxm_dataset_test.txt.zip
'''

from typing import List
import json
import os
from tqdm import tqdm
import fasttext
import fasttext.util
import pickle
import stemmer


def normalize(collection: List[str]) -> List[str]:
    '''Copied from utils.text_processing'''
    return stemmer.stemWords(collection)

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
                    all_words = line[1:].split(',')
                elif line.startswith('TR'):
                    line = line.split(',')
                    track_id = line[0]
                    word_dict = {int(id): int(freq) for id_freq in line[2:] for id, freq in [id_freq.split(':')]}
                    lyrics_dict[track_id] = word_dict

    return lyrics_dict, all_words

def make_inverted_index(lyrics_word_dict: dict) -> dict:
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

def save_lyrics_inverted_index(lyrics_inverted_index, path='data/lyrics_inverted_word.pkl'):
    with open(path, 'wb') as file:
        pickle.dump(lyrics_inverted_index, file)
    print(f"lyrics_inverted_index saved as pickle at {path}")


def create_lyrics_similarity_dict(all_words, embeddings, save_path='lyrics_similarity_dict.json', batch_size=100):
    '''
    Create a dictionary with similar tokens to those in the lyrics.
    Similar tokens are those with score > 0.7.
    Progress is saved every batch_size words.
    If interrupted, resumes from the saved file.
    '''

    # Load existing dictionary if the file exists
    if os.path.exists(save_path):
        with open(save_path, 'r', encoding='utf-8') as f:
            lyrics_similarity_dict = json.load(f)
        processed_words = set(lyrics_similarity_dict.keys())
        print(f"Loaded {len(processed_words)} processed words from {save_path}")
    else:
        lyrics_similarity_dict = {}
        processed_words = set()

    # Get words to process
    words_to_process = set(all_words) - processed_words

    # Iterate over remaining words with a progress bar
    for i, word in enumerate(tqdm(words_to_process, desc="Processing words", initial=len(processed_words), total=len(all_words))):
        # Get all words with a similarity score of >0.7
        similar_words = {word.lower() for score, word in embeddings.get_nearest_neighbors(word, k=20) if score > 0.7}
        extra_tokens = set(normalize(similar_words)) & set(all_words) - {word}

        # Add the similar words to the dictionary
        lyrics_similarity_dict[word] = list(extra_tokens)  # Convert set to list for JSON compatibility

        # Save the dictionary to file every batch_size iterations
        if (i + 1) % batch_size == 0:
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(lyrics_similarity_dict, f, ensure_ascii=False, indent=2)

    # Final save to ensure all data is written
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(lyrics_similarity_dict, f, ensure_ascii=False, indent=2)
    print(f"Final save complete. {len(lyrics_similarity_dict)} words processed.")

    return lyrics_similarity_dict

def save_lyrics_similarity_dict(lyrics_similarity_dict, path='data/lyrics_similarity_dict.pkl'):
    '''Function to save the lyrics_similarity_dict as a pickle file'''
    with open(path, 'wb') as file:
        pickle.dump(lyrics_similarity_dict, file)
    print(f"lyrics_similarity_dict saved as pickle at {path}")

if __name__ == '__main__':

    # Input paths
    lyrics_test_path = 'data/mxm_dataset_test.txt'
    lyrics_train_path = 'data/mxm_dataset_train.txt'

    # Output
    lyrics_all_words_path = 'data/lyrics_all_words.txt'
    lyrics_inverted_index_path = 'data/lyrics_inverted_idx.pkl'

    # Load the data
    lyrics_dict_idx, all_words = read_lyrics(lyrics_train_path, lyrics_test_path)

    # Make mappings from words to indices, where idx starts at 1
    word_to_idx = {word: index+1 for index, word in enumerate(all_words)}
    index_to_word = {index+1: word for index, word in enumerate(all_words)}

    # Create a dictionary with words instead of indices
    lyrics_dict_word = {track_id: {index_to_word[int(id)]: int(freq) for id, freq in word_dict.items()} for track_id, word_dict in lyrics_dict_idx.items()}

    # Make inverted index
    inverted_index = make_inverted_index(lyrics_dict_word)

    # Save the inverted index
    save_lyrics_inverted_index(inverted_index)

    # Load the data
    # with open(lyrics_inverted_index_path, 'rb') as file:
    #     inverted_index = pickle.load(file)

    make_fasttext_model = False
    if make_fasttext_model:
        # Load the fasttext modelimport fasttext
        fasttext.util.download_model('en', if_exists='ignore')
        ft = fasttext.load_model('cc.en.300.bin')

        # Load / create the lyrics similarity dictionary (it is iteratively created as a json so that it can be resumed)
        lyrics_similarity_dict = create_lyrics_similarity_dict(all_words, ft, save_path='data/lyrics_similarity_dict.json', batch_size=100)

        # Save the lyrics_similarity_dict as a pickle for faster loading
        save_lyrics_similarity_dict(lyrics_similarity_dict)



