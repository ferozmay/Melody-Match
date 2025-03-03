import pickle

# LOAD DICTS
lyrics_test_path = 'data/mxm_dataset_test.txt'
lyrics_train_path = 'data/mxm_dataset_train.txt'

# Output
lyrics_all_words_path = 'data/lyrics_all_words.txt'
lyrics_inverted_index_path = 'data/lyrics_inverted_idx.pkl'

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

    return lyrics_dict, set(all_words)

# Load the data
lyrics_dict_idx, all_words = read_lyrics(lyrics_train_path, lyrics_test_path)

# Make mappings from words to indices, where idx starts at 1
word_to_idx = {word: index+1 for index, word in enumerate(all_words)}
index_to_word = {index+1: word for index, word in enumerate(all_words)}

# Create a dictionary with words instead of indices
lyrics_dict_word = {track_id: {index_to_word[int(id)]: int(freq) for id, freq in word_dict.items()} for track_id, word_dict in lyrics_dict_idx.items()}

# Make inversed index
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

inverted_index = make_inverted_index(lyrics_dict_word)

# Save the data
def save_lyrics_inverted_index(lyrics_inverted_index, path='data/lyrics_inverted_word.pkl'):
    with open(path, 'wb') as file:
        pickle.dump(lyrics_inverted_index, file)
    print(f"lyrics_inverted_index saved as pickle at {path}")

# Save the inverted index
save_lyrics_inverted_index(inverted_index)