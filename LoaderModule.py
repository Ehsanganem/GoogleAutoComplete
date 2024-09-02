import os
import json
from collections import defaultdict
from functools import lru_cache

from ScoreFunction import sentences_score
import timeit

class LoaderModule:
    @lru_cache(maxsize=128)  # Cache the results of the search

    def __init__(self):
        self.text_data = []

    def load_text_files(self, directory):
        """Loads and preprocesses text files from a given directory."""
        self.text_data = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line_num, line in enumerate(f, 1):
                            original_text = line.strip()
                            preprocessed_text = self.preprocess_text(original_text)
                            self.text_data.append({
                                'original': original_text,
                                'preprocessed': preprocessed_text,
                                'source_file': file,
                                'line_number': line_num
                            })
        return self.text_data

    def preprocess_text(self, text):
        """Preprocesses a given text by lowercasing and removing punctuation."""
        import string
        return text.lower().translate(str.maketrans('', '', string.punctuation)).strip()

    def save_data(self, filename):
        """Saves the preprocessed text data to a JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.text_data, f)

    def load_data(self, filename):
        """Loads preprocessed text data from a JSON file."""
        with open(filename, 'r', encoding='utf-8') as f:
            self.text_data = json.load(f)
        return self.text_data

    def search(self, query, inverted_index, top_n=5, threshold=80):
        """Search for relevant documents based on the query and rank them by likeness score."""
        preprocessed_query = self.preprocess_text(query)
        query_words = preprocessed_query.split()

        if len(query_words) < 2:
            # If the query is a single word, treat the whole word as the search term
            query_ngrams = [tuple(query_words)]
        else:
            # Otherwise, create n-grams as usual
            query_ngrams = [tuple(query_words[i:i + 2]) for i in range(len(query_words) - 1)]

        # Retrieve documents using fuzzy matching
        retrieved_documents = []
        for ngram in query_ngrams:
            retrieved_documents.extend(inverted_index.retrieve_documents(ngram, threshold=threshold))

        # Remove duplicates
        retrieved_documents = list(set(retrieved_documents))

        # Score the retrieved documents based on likeness
        scored_results = []
        for doc in retrieved_documents:
            score = sentences_score(preprocessed_query, doc)
            scored_results.append((doc, score))

        # Sort results by score in descending order and return the top N results
        scored_results.sort(key=lambda x: x[1], reverse=True)
        return scored_results[:top_n]

