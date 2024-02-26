import csv
import os

import requests

from cambridge_parser import get_word


def parse_word_data(word, data):
    # Prepare the row data for CSV
    row = {
        'IMG': f'<img src="{word}.jpg">',
        'POS': ', '.join(data['POS']),
        'Word': word,
        'Meaning': ', '.join(data['data']['definitions']),
        'IPA': data['data']['UK_IPA'][0][0],
        'Pronunciation': f'[sound:{word}.mp3]',
        'Example': ', '.join(data['data']['examples'][0]),
        'Translation': '-'
    }
    return row


def download_pronunciation(word, url):
    # Set headers to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Download the pronunciation file
    response = requests.get(url, headers=headers)
    word = word.replace('/', '|')

    with open(f'data/Pronunciation/{word}.mp3', 'wb') as f:
        f.write(response.content)


def main():
    # Create the Pronunciation directory if it doesn't exist
    if not os.path.exists('data/Pronunciation'):
        os.makedirs('data/Pronunciation')

    # Open the words file and the output CSV file
    with open('data/words.txt', 'r') as words_file, open('data/words.csv', 'w', newline='') as csv_file:
        # Prepare the CSV writer
        fieldnames = ['IMG', 'POS', 'Word', 'Meaning', 'IPA', 'Pronunciation', 'Example', 'Translation']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        # Process each word
        for word in words_file:
            word = word.strip()
            print(f"[{word}]")
            word_data = get_word(word)
            word, data_list = next(iter(word_data[0].items()))
            data = data_list[0]
            row = parse_word_data(word, data)
            writer.writerow(row)

            download_pronunciation(word, data['data']['UK_audio_links'][0][0])


if __name__ == '__main__':
    main()
