import os
import sys

# Adjust the path to allow imports from the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from LoaderModule import LoaderModule

def main():
    # Set the directory to the Tests folder
    directory = os.path.join(os.path.dirname(__file__), '')

    # Create an instance of the LoaderModule
    processor = LoaderModule()

    # Load and preprocess text data from the Tests folder
    processor.load_text_files(directory)

    # Save the preprocessed data to a file
    processor.save_data('preprocessed_data.json')

    # Optionally, load the data back to verify it was saved correctly
    loaded_data = processor.load_data('preprocessed_data.json')

    # Display the loaded and preprocessed data
    for entry in loaded_data:
        print(f"File: {entry['source_file']}, Line: {entry['line_number']}")
        print(f"Original: {entry['original']}")
        print(f"Preprocessed: {entry['preprocessed']}")
        print("-" * 40)

if __name__ == "__main__":
    main()
