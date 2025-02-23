from typing import List
from nltk.stem import PorterStemmer
import Stemmer
from collections import Counter
import re

alphanum = r"[a-zA-Z0-9_-]*"
non_alphanum = r"[^a-zA-Z0-9_-]"

stemmer = PorterStemmer()
stemmer = Stemmer.Stemmer("english")
# load stopwords
with open("./utils/stopwords.txt", "r") as stopwords_file:
    stopwords = set(stopwords_file.read().strip().split("\n"))


def tokenize_text(text: str) -> List[str]:
    """
    lowercases everything, converts non-alphanumeric chars into newlines
    returns an array of tokens, split by newline (drops empty strings)
    """
    text = text.lower()
    text = re.sub(non_alphanum, "\n", text)
    return list(filter(lambda token: bool(token), text.split("\n")))


def remove_stopwords(collection: List[str]) -> List[str]:
    """
    Drops all entries that are in the stopword list
    """
    return list(filter(lambda token: token not in stopwords, collection))

def normalize(collection: List[str]) -> List[str]:
    return stemmer.stemWords(collection)


def process_text(text: str):
    tokens = tokenize_text(text)
    # tokens = remove_stopwords(tokens)
    tokens = normalize(tokens)
    return " ".join(tokens)
