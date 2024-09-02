import os
import timeit
from LoaderModule import LoaderModule
from ScoreFunction import sentences_score


def display_completions(completions):
    """Display the top 5 completions with their scores, sorted by score and alphabetically."""
    if not completions:
        print("No matching completions found.")
        return

    # Sort by score (higher is better), then alphabetically by the string
    completions.sort(key=lambda x: (-x[3], x[1]))

    print("\nTop 5 completions:")
    for i, (file_name, string, line_num, score) in enumerate(completions[:5]):
        print(f"{i + 1}. Score: {score} - File: {file_name} - Line: {line_num} - String: {string}")


def main():
    loader = LoaderModule()

    # Load the reverse index from a preprocessed file
    print("Loading reverse index from MessagePack...")
    loader.load_reverse_index_from_msgpack('reverse_index.msgpack')

    user_input = ""

    while True:
        # Continue receiving input
        new_input = input(f"Current input: {user_input}\nEnter next characters (or type '#' to reset): ").strip()

        if new_input == "#":
            print("Resetting input...")
            user_input = ""
            continue

        user_input = user_input + new_input

        # Time the search using timeit
        def search():
            return loader.search(user_input)

        search_duration = timeit.timeit(search, number=1)

        # Search for matching original strings and file names
        matching_results = search()

        # If no results are found, inform the user
        if not matching_results:
            print("No matching results found.")
            continue

        # Rank the results using the sentences_score function
        scored_results = [(file_name, string, line_num, sentences_score(user_input, string))
                          for file_name, string, line_num in matching_results]

        # Display the search duration and the top 5 completions
        print(f"Search completed in {search_duration:.4f} seconds.")
        display_completions(scored_results)


if __name__ == "__main__":
    main()
