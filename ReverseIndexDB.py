class FileMetadata:
    def __init__(self, file_name):
        self.file_name = file_name
        self.strings = []  # List to store tuples of (original_str, processed_str)

    def add_string(self, original_str):
        # Process the string before saving
        processed_str = self.process_text(original_str)
        self.strings.append((original_str, processed_str))  # Append the strings as a tuple

    @staticmethod
    def process_text(text):
        """Process the text by lowercasing and removing punctuation."""
        import string
        return text.lower().translate(str.maketrans('', '', string.punctuation)).strip()


class ReverseIndex:
    def __init__(self):
        self.index = {}

    def add_word(self, word, file_name, original_str):
        if word not in self.index:
            self.index[word] = []

        # Attempt to find an existing FileMetadata object for this file
        existing_metadata = next((metadata for metadata in self.index[word] if metadata.file_name == file_name), None)

        if existing_metadata:
            # Add the original string to the existing FileMetadata (it will be processed internally)
            existing_metadata.add_string(original_str)
        else:
            # Create new FileMetadata and add it to the list
            new_metadata = FileMetadata(file_name)
            new_metadata.add_string(original_str)
            self.index[word].append(new_metadata)

    def get_files_for_word(self, word):
        """Retrieve all file metadata objects for a given word."""
        return self.index.get(word, [])


