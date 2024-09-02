import os
import json
from collections import defaultdict


class LoaderModule:
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


