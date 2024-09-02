from fuzzywuzzy import fuzz

SIMILARITY_THRESHOLD = 70


def search_files(input_string: str, words_map: dict) -> list:
    """
    This function searches for files based on the input string and the words map.
    :param input_string:
    :param words_map:
    :return:  A list of files that match the input string.
    """
    files = set()
    is_first = True
    for input_word in input_string.split():
        for word in words_map.keys():
            similarity_score = fuzz.ratio(input_word, word)
            if similarity_score > SIMILARITY_THRESHOLD:
                if is_first:
                    files = words_map[word]
                    is_first = False
                else:
                    files = files.intersection(words_map[word])
    return list(files)





