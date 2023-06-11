import csv
import re
import time
import sys

def load_dictionary(dictionary_file):
    dictionary = {}
    with open(dictionary_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            english_word = row[0]
            french_word = row[1]
            dictionary[english_word] = french_word
    return dictionary

def replace_words(input_file, find_words_file, dictionary_file, output_file, frequency_file):
    # Load the dictionary
    dictionary = load_dictionary(dictionary_file)

    # Read the find words list
    with open(find_words_file, 'r') as file:
        find_words = [word.strip() for word in file.readlines()]

    # Read the input text file
    with open(input_file, 'r') as file:
        content = file.read()

    # Initialize counters
    num_replacements = 0
    replacements_freq = {}

    # Replace words while maintaining case
    start_time = time.time()
    for word in find_words:
        if word in dictionary:
            replacement = dictionary[word]
            # Preserve the case of the original word
            if word.islower():
                replacement = replacement.lower()
            elif word.isupper():
                replacement = replacement.upper()
            elif word.istitle():
                replacement = replacement.title()

            # Replace the word using regex with word boundaries
            pattern = r'\b' + re.escape(word) + r'\b'
            content, replacements = re.subn(pattern, replacement, content)
            num_replacements += replacements

            if word in replacements_freq:
                replacements_freq[word] += replacements
            else:
                replacements_freq[word] = replacements

    # Save the processed file
    with open(output_file, 'w') as file:
        file.write(content)

    # Save the frequency file
    with open(frequency_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['English word', 'French word', 'Frequency'])
        for word, freq in replacements_freq.items():
            writer.writerow([word, dictionary[word], freq])

    end_time = time.time()
    processing_time = end_time - start_time

    # Get memory usage
    memory_usage = sys.getsizeof(content)

    print("Processing completed successfully.")
    print("Number of word replacements:", num_replacements)
    print("Time taken to process (seconds):", processing_time)
    print("Memory used (bytes):", memory_usage)



# Usage example
replace_words('t8.shakespeare.txt', 'find_words.txt', 'french_dictionary.csv', 'output.txt','frequency.csv')
