import os
import json
from collections import defaultdict
from functools import lru_cache
from ReverseIndexDB import ReverseIndex, FileMetadata


class LoaderModule:
    def __init__(self):
        self.reverse_index = ReverseIndex()
        self.processed_files = set()
        self.checkpoint_file = "checkpoint.json"

    def load_text_files(self, directory):
        """Loads text files from a given directory and fills the reverse index."""
        self.load_checkpoint()  # Load the previous state if it exists

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.txt') and file not in self.processed_files:
                    print(f"Processing file: {file}")
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line_num, line in enumerate(f, 1):
                            preprocessed_text = self.preprocess_text(line.strip())
                            words = preprocessed_text.split()
                            for index, word in enumerate(words):
                                self.reverse_index.add_word(word, file, line_num, index)
                    # Mark this file as processed
                    self.processed_files.add(file)
                    # Save the current state after processing each file
                    self.save_checkpoint()
                    print(f"File {file} done processing")
        return self.reverse_index

    def preprocess_text(self, text):
        """Preprocesses text by lowercasing and removing punctuation."""
        import string
        return text.lower().translate(str.maketrans('', '', string.punctuation)).strip()

    def save_index(self, filename):
        """Saves the reverse index to a JSON file."""
        index_data = {}

        # Convert the reverse index to a JSON-compatible format
        for word, file_metadata_list in self.reverse_index.index.items():
            index_data[word] = []
            for metadata in file_metadata_list:
                index_data[word].append({
                    'file_name': metadata.file_name,
                    'locations': list(metadata.locations)  # Convert set to list for JSON compatibility
                })

        # Write the JSON data to the file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, ensure_ascii=False, indent=4)

    def load_index(self, filename):
        """Loads the reverse index from a JSON file."""
        with open(filename, 'r', encoding='utf-8') as f:
            index_data = json.load(f)

        # Clear the existing index to avoid duplicates
        self.reverse_index.index.clear()

        # Rebuild the reverse index from the JSON data
        for word, file_metadata_list in index_data.items():
            for file_metadata in file_metadata_list:
                file_name = file_metadata['file_name']
                locations = set(tuple(loc) for loc in file_metadata['locations'])

                # Check if this file already exists in the index for this word
                existing_metadata = next((metadata for metadata in self.reverse_index.index.get(word, []) if
                                          metadata.file_name == file_name), None)

                if existing_metadata:
                    # Merge locations if the file already exists
                    existing_metadata.locations.update(locations)
                else:
                    # Otherwise, create a new FileMetadata object and add it
                    new_metadata = FileMetadata(file_name)
                    new_metadata.locations = locations
                    self.reverse_index.index.setdefault(word, []).append(new_metadata)

        return self.reverse_index

    def save_checkpoint(self):
        """Saves the current state (reverse index and processed files) to a checkpoint file."""
        checkpoint_data = {
            'reverse_index': {word: [{'file_name': metadata.file_name, 'locations': list(metadata.locations)}
                                     for metadata in file_metadata_list]
                              for word, file_metadata_list in self.reverse_index.index.items()},
            'processed_files': list(self.processed_files)
        }

        with open(self.checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint_data, f, ensure_ascii=False, indent=4)
        print(f"Checkpoint saved. Processed {len(self.processed_files)} files.")

    def load_checkpoint(self):
        """Loads the last saved state from the checkpoint file, if it exists."""
        if os.path.exists(self.checkpoint_file):
            with open(self.checkpoint_file, 'r', encoding='utf-8') as f:
                checkpoint_data = json.load(f)

            # Load the reverse index
            for word, file_metadata_list in checkpoint_data['reverse_index'].items():
                for file_metadata in file_metadata_list:
                    file_name = file_metadata['file_name']
                    locations = set(tuple(loc) for loc in file_metadata['locations'])

                    existing_metadata = next((metadata for metadata in self.reverse_index.index.get(word, []) if
                                              metadata.file_name == file_name), None)

                    if existing_metadata:
                        existing_metadata.locations.update(locations)
                    else:
                        new_metadata = FileMetadata(file_name)
                        new_metadata.locations = locations
                        self.reverse_index.index.setdefault(word, []).append(new_metadata)

            # Load the list of processed files
            self.processed_files = set(checkpoint_data['processed_files'])
            print(f"Loaded checkpoint. Resuming from {len(self.processed_files)} processed files.")


# Example usage
if __name__ == "__main__":
    loader = LoaderModule()

    # Load and preprocess text files from the specified directory
    reverse_index = loader.load_text_files('Text Archive')

    # Save the reverse index to a JSON file
    loader.save_index('reverse_index.json')

    # Load the index back to check if it was saved correctly
    reverse_index = loader.load_index('reverse_index.json')

    # Print the reverse index to verify its contents
    print("Loaded Reverse Index Contents:")
    for word, file_metadata_list in reverse_index.index.items():
        print(f"Word: '{word}'")
        for metadata in file_metadata_list:
            print(f"  File: {metadata.file_name}, Locations: {metadata.locations}")
