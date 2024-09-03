import os
import time
from LoaderModule import LoaderModule
from ScoreFunction import sentences_score


def main():
    loader = LoaderModule()

    # Load the reverse index from a preprocessed file
    print("Loading reverse index from MessagePack...")
    loader.load_reverse_index_from_msgpack('reverse_index.msgpack')

    user_input = ""
    new_input = ""
    while new_input != "exit":
        # Continue receiving input
        new_input = input(f"Current input: {user_input}\nEnter next characters (or type '#' to reset): ").strip()
        if new_input == "exit":
            exit(0)
        if new_input == "#":
            print("Resetting input...")
            user_input = ""
            continue

        user_input += new_input

        # Time the search using timeit
        start = time.time()
        # Search for matching original strings and file names
        matching_results = loader.search(user_input.strip())

        # If no results are found, inform the user
        if not matching_results:
            print("No matching results found.")
            continue

        # Rank the results using the sentences_score function
        scored_results = []
        for file_name, full_string, line_num in matching_results:
            score = sentences_score(user_input, full_string)  # Use the full string for scoring
            scored_results.append((file_name, full_string, line_num, score))

        # Sort by score in descending order and display the top 5 completions
        scored_results.sort(key=lambda x: x[3], reverse=True)
        stop = time.time()
        elapsed = stop - start
        print(f"Time for search was {elapsed}")
        display_completions(scored_results)


def display_completions(scored_results):
    """Displays the top 5 results."""
    print("\nTop 5 completions:")
    for i, (file_name, full_string, line_num, score) in enumerate(scored_results[:5]):
        print(f"{i + 1}. Score: {score} - File: {file_name} - Line: {line_num} - String: {full_string}")

    print("\n")


if __name__ == "__main__":
    main()


