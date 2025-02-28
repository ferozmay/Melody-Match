'''Save a dictionary with similar words for all 5000 words in lyrics'''
import json
import os
from tqdm import tqdm
from utils.text_processing import normalize
import fasttext
import fasttext.util
import pickle

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

# Function to save the lyrics_similarity_dict as a pickle file
def save_lyrics_similarity_dict(lyrics_similarity_dict, path='data/lyrics_similarity_dict.pkl'):
    with open(path, 'wb') as file:
        pickle.dump(lyrics_similarity_dict, file)
    print(f"lyrics_similarity_dict saved as pickle at {path}")


if __name__ == '__main__':

    # Load the fasttext modelimport fasttext
    ft = fasttext.load_model('cc.en.300.bin')

    # Load all words
    with open('data/all_words.txt', 'r', encoding='utf-8') as f:
        all_words = f.read().splitlines()

    # Load the lyrics_inverted_index
    lyrics_similarity_dict = create_lyrics_similarity_dict(all_words, ft, save_path='data/lyrics_similarity_dict.json', batch_size=100)

    # Save the lyrics_similarity_dict as a pickle for faster loading
    save_lyrics_similarity_dict(lyrics_similarity_dict)