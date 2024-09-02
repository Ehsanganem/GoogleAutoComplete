class FileMetadata:
    def __init__(self, file_name):
        self.file_name = file_name
        self.locations = set()  # Set of (line_number, index_within_line) tuples

    def add_location(self, line_number, index_within_line):
        self.locations.add((line_number, index_within_line))

    def merge(self, other):
        """Merge another FileMetadata's locations if the file names match."""
        if self.file_name == other.file_name:
            self.locations.update(other.locations)

    def __eq__(self, other):
        """Compare FileMetadata objects by file name."""
        if isinstance(other, FileMetadata):
            return self.file_name == other.file_name
        return False

    def __hash__(self):
        """Hash FileMetadata by file name to use in sets and dicts."""
        return hash(self.file_name)


class ReverseIndex:
    def __init__(self):
        self.index = {}

    def add_word(self, word, file_name, line_number, index_within_line):
        if word not in self.index:
            self.index[word] = []

        # Attempt to find existing FileMetadata object for this file
        existing_metadata = next((metadata for metadata in self.index[word] if metadata.file_name == file_name), None)

        if existing_metadata:
            # Add location to the existing FileMetadata
            existing_metadata.add_location(line_number, index_within_line)
        else:
            # Create new FileMetadata and add it to the list
            new_metadata = FileMetadata(file_name)
            new_metadata.add_location(line_number, index_within_line)
            self.index[word].append(new_metadata)

    def get_files_for_word(self, word):
        """Retrieve all file metadata objects for a given word."""
        return self.index.get(word, [])




