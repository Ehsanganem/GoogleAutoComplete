import os
import msgpack  # MessagePack for faster serialization
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from ReverseIndexDB import ReverseIndex, FileMetadata
from SearchFiles import search_files

class LoaderModule:
    @lru_cache(maxsize=128)
    def __init__(self):
        self.reverse_index = ReverseIndex()
        self.processed_files = set()
        self.batch_size = 100  # Process files in batches

    def load_text_files(self, directory):
        """Loads text files from a given directory and fills the reverse index."""
        all_files = [os.path.join(root, file)
                     for root, dirs, files in os.walk(directory)
                     for file in files if file.endswith('.txt') and file not in self.processed_files]

        # Debugging: Check if files are being collected correctly
        if not all_files:
            print(f"No files found in directory: {directory}")

        # Process files in batches with multi-threading
        with ThreadPoolExecutor(max_workers=16) as executor:
            executor.map(self.process_file, all_files)

        return self.reverse_index

    def process_file(self, file_path):
        """Processes a single file and updates the reverse index."""
        file_name = os.path.basename(file_path)
        print(f"Processing file: {file_name}")
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                for word in line.split():
                    self.reverse_index.add_word(word, file_name, line, line_num)
        self.processed_files.add(file_name)
        print(f"File {file_name} done processing")

    def save_index_msgpack(self, filename):
        """Saves the reverse index to a MessagePack file."""
        with open(filename, 'wb') as f:
            for word, metadata_list in self.reverse_index.index.items():
                for metadata in metadata_list:
                    msgpack_entry = {
                        'word': word,
                        'fn': metadata.file_name,
                        'ss': [{'os': original, 'ps': processed, 'ln': line_num}
                               for original, processed, line_num in metadata.strings]
                    }
                    # Stream the data entry by entry to the file
                    packed_data = msgpack.packb(msgpack_entry, use_bin_type=True)
                    f.write(packed_data)
        print(f"Reverse index saved to {filename} in MessagePack format.")

    def load_reverse_index_from_msgpack(self, filename):
        """Loads the reverse index from a MessagePack file into the ReverseIndex instance."""

        def dict_to_metadata(metadata_dict):
            file_name = metadata_dict['fn']
            strings = [(entry['os'], entry['ps'], entry['ln']) for entry in metadata_dict['ss']]
            metadata = FileMetadata(file_name)
            metadata.strings.extend(strings)
            return metadata

        with open(filename, 'rb') as f:
            unpacker = msgpack.Unpacker(f, raw=False)
            for msgpack_entry in unpacker:
                word = msgpack_entry['word']
                metadata = dict_to_metadata(msgpack_entry)
                if word not in self.reverse_index.index:
                    self.reverse_index.index[word] = []
                self.reverse_index.index[word].append(metadata)

        print(f"Reverse index loaded from {filename}.")

    def search(self, query, top_n=5, threshold=80):
        """Search for relevant documents based on the query and rank them by likeness score."""
        return search_files(query, self.reverse_index)
