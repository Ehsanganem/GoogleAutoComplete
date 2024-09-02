from fuzzywuzzy import fuzz
from ReverseIndexDB import ReverseIndex

SIMILARITY_THRESHOLD = 70

def search_files(input_string: str, reverse_index: ReverseIndex) -> list:
    """
    This function searches for the original strings based on the input string and the reverse index.
    :param input_string: The string to search for.
    :param reverse_index: The ReverseIndex object containing the indexed words and associated files and strings.
    :return: A list of tuples containing the file name, original string, and line number.
    """
    matched_strings = set()
    is_first = True

    # Split the input string into words and process them
    input_words = input_string.split()

    # Iterate over each word in the input string
    for input_word in input_words:
        current_matched_strings = set()

        # Iterate over all words in the reverse index
        for word, metadata_list in reverse_index.index.items():
            similarity_score = fuzz.ratio(input_word, word)
            if similarity_score > SIMILARITY_THRESHOLD:
                # If the word is a match, add its associated original strings to the current_matched_strings set
                for metadata in metadata_list:
                    for original, _, line_num in metadata.strings:
                        current_matched_strings.add((metadata.file_name, original, line_num))

        # Combine matched strings with existing results
        if is_first:
            matched_strings = current_matched_strings
            is_first = False
        else:
            matched_strings = matched_strings.intersection(current_matched_strings)

        # If at any point no strings match, we can return early
        if not matched_strings:
            return []

    return list(matched_strings)
