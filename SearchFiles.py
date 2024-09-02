from fuzzywuzzy import fuzz
from ReverseIndexDB import ReverseIndex

SIMILARITY_THRESHOLD = 70

def search_files(input_string: str, reverse_index: ReverseIndex) -> list:
    """
    This function searches for the original strings based on the input string and the reverse index.
    :param input_string: The string to search for.
    :param reverse_index: The ReverseIndex object containing the indexed words and associated files and strings.
    :return: A list of tuples (file_name, original_line) that match the input string.
    """
    matched_results = set()
    is_first = True

    # Split the input string into words and process them
    input_words = input_string.split()

    # Iterate over each word in the input string
    for input_word in input_words:
        current_matched_results = set()

        # Iterate over all words in the reverse index
        for word in reverse_index.index.keys():
            similarity_score = fuzz.ratio(input_word, word)
            if similarity_score > SIMILARITY_THRESHOLD:
                # If the word is a match, add its associated file name and original string to the current set
                for metadata in reverse_index.index[word]:
                    for original, _ in metadata.strings:
                        current_matched_results.add((metadata.file_name, original))

        # Combine matched results with existing results
        if is_first:
            matched_results = current_matched_results
            is_first = False
        else:
            matched_results = matched_results.intersection(current_matched_results)

        # If at any point no results match, we can return early
        if not matched_results:
            return []

    return list(matched_results)


