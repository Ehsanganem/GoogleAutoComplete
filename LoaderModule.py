import os
import json
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache

from ReverseIndexDB import ReverseIndex
from ScoreFunction import sentences_score
import timeit

class LoaderModule:
    @lru_cache(maxsize=128)  # Cache the results of the search

    def __init__(self):
        self.text_data = []
        self.reverse_index = ReverseIndex()
        self.processed_files = set()
        self.batch_size = 100  # Process files in batches

    def load_text_files(self, directory):
        """Loads text files from a given directory and fills the reverse index."""

        # Collect all files to process
        all_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.txt') and file not in self.processed_files:
                    all_files.append(os.path.join(root, file))

        # Process files in batches with multi-threading
        for i in range(0, len(all_files), self.batch_size):
            batch = all_files[i:i + self.batch_size]
            with ThreadPoolExecutor(max_workers=16) as executor:
                executor.map(self.process_file, batch)


        return self.reverse_index

    def process_file(self, file_path):
        """Processes a single file and updates the reverse index."""
        file_name = os.path.basename(file_path)
        print(f"Processing file: {file_name}")
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                words = line.split()
                for index, word in enumerate(words):
                    self.reverse_index.add_word(word, file_name, line)

        # Mark this file as processed
        self.processed_files.add(file_name)
        print(f"File {file_name} done processing")

    def save_data(self, filename):
        """Saves the preprocessed text data to a JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.text_data, f)

    def load_data(self, filename):
        """Loads preprocessed text data from a JSON file."""
        with open(filename, 'r', encoding='utf-8') as f:
            self.text_data = json.load(f)
        return self.text_data

    def preprocess_text(self, text):
        """Preprocesses a given text by lowercasing and removing punctuation."""
        import string
        return text.lower().translate(str.maketrans('', '', string.punctuation)).strip()

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

    def save_index_json(self, filename):
        """Saves the reverse index to a JSON file."""

        def metadata_to_dict(metadata):
            return {
                'file_name': metadata.file_name,
                'strings': [{'original': original, 'processed': processed} for original, processed in metadata.strings]
            }

        reverse_index_data = {
            word: [metadata_to_dict(metadata) for metadata in metadata_list]
            for word, metadata_list in self.reverse_index.index.items()  # Adjusted to use self.index directly
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(reverse_index_data, f, ensure_ascii=False, indent=4)
        print(f"Reverse index saved to {filename} in JSON format.")

