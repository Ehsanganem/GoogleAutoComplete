# AutoComplete Engine for Google-like Search

## Introduction

This project implements an autocomplete engine to improve the user experience in a search engine, inspired by the Google autocomplete feature. The engine allows users to type a partial sentence and receive five of the best sentence completions from a dataset of articles, documentation, and tech-related files. The system is designed to handle a large corpus of documents and provide fast, accurate sentence completions, supporting common string corrections such as character replacement, insertion, and deletion.

### Key Features

- **Sentence Autocompletion**: The engine supports partial sentence matching and suggests completions based on a preprocessed dataset.
- **Fuzzy Matching**: The system supports string corrections (e.g., replacement, insertion, or deletion of one character) to match the user’s input with the best possible sentence.
- **Multithreading for Efficiency**: Parallel processing is implemented using Python's `ThreadPoolExecutor` to improve the speed of text file processing and searching.
- **Custom Scoring Function**: The sentences are ranked based on a custom scoring function that calculates how closely a sentence matches the input string.
- **Offline and Online Modes**:
  - **Offline Mode**: Preprocesses text files into a searchable index.
  - **Online Mode**: Waits for user input and returns the best completions in real-time.

## Task Overview

The task is split into two main functionalities:

1. **Initialization Function**: The engine processes a list of text sources, prepares an index based on the sentences within them, and stores the results for quick access during the autocomplete process.
2. **Completion Function**: Given a user's input string, the system returns the top five completions based on a custom scoring algorithm.

## How It Works

### 1. **Initialization**

The text files are processed and indexed using a reverse index structure, which stores the words and the corresponding sentences they belong to. The index is serialized using the efficient `MessagePack` format for fast retrieval.

### 2. **Completion Process**

Once the user starts typing, the system searches the indexed sentences and computes a score for each possible completion. The top five completions are ranked based on their score and displayed to the user.

### 3. **String Matching & Correction**

The system supports matching even when the input string has one of the following errors:
- **Character Replacement**: One character is different.
- **Character Insertion**: An extra character is added.
- **Character Deletion**: A character is missing.

The matching strings are ranked based on how closely they align with the input, using a custom scoring system that takes these corrections into account.

## Installation

### Prerequisites

- Python 3.6+
- `rapidfuzz` for string similarity
- `msgpack` for fast serialization
- `concurrent.futures` for parallel processing

### Install Dependencies

To install the required dependencies, run:

### bash
pip install rapidfuzz msgpack
### Scoring System
Exact Match: The base score is twice the number of matched characters.
Character Replacement: Penalties are applied for each replaced character:
1st replacement: -5 points
2nd replacement: -4 points
3rd replacement: -3 points
4th replacement: -2 points
5th replacement and onward: -1 point
Character Insertion/Deletion: -2 points are deducted for an insertion or deletion, with higher penalties for the first 4 characters.