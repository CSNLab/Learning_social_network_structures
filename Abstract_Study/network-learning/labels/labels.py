#!/usr/bin/env python

from __future__ import print_function
from string import ascii_uppercase
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import csv


letters = set(ascii_uppercase) - set('IOQUVXYZ')
airport_df = pd.read_csv('airports.csv',
                         names=['id', 'name', 'city', 'country', 'IATA', 'ICAO',
                                'latitude', 'longitude', 'altitude', 'timezone',
                                'DST', 'tz', 'type', 'source'])
all_airports = set(airport_df['IATA'])
with open('words.txt', 'r') as infile:
    common_words = set([word.upper() for word in infile.read().splitlines()])

# excluding airports and words with repeated characters
results = set()
for c1 in letters:
    for c2 in letters:
        for c3 in letters:
            if c1 == c2 or c2 == c3 or c1 == c3:
                continue
            if (c1 + c2 + c3) in all_airports or (c1 + c2 + c3) in common_words:
                continue
            results.add(c1 + c2 + c3)


def look_similar(word, word_set, strict=False):
    if strict:  # when strict, similar == containing >1 same letters
        for other_word in word_set:
            if len(set(other_word).union(set(word))) < len(word) + len(other_word) - 1:
                return True
    else:  # when not strict, similar == containing >1 same letters at the same positions
        for i in range(len(word)):
            for letter in ascii_uppercase:
                similar_word = word[:i] + letter + word[i + 1:]
                if similar_word in word_set:
                    return True
    return False


# excluding words that looks like a busy airport
busy_df = pd.read_csv('busiest_airports.csv')
busy_airports = set(busy_df['IATA'])
less_results = set()
for word in results:
    if not look_similar(word, busy_airports):
        less_results.add(word)
results = less_results


def get_google_results(words):
    # scrape google search results, return {word: number_of_results}
    google = 'https://www.google.com/search?num=1&q='
    session = requests.Session()
    results_dict = {}
    for word in words:
        got_result = False
        try:
            while not got_result:
                r = session.get(google + word)
                stats = BeautifulSoup(r.text, 'html.parser').find(id='resultStats')
                if stats is not None:
                    got_result = True
                else:
                    session = requests.Session()
        except Exception as e:
            print('Error with ' + word + ':', e)
        else:
            number = str(stats.text).split()[1]
            number = int(number.replace(',', ''))
            results_dict[word] = number
            print(word, number)
        time.sleep(5)
    return results_dict


# get google results and write to frequency.csv
freq_dict = get_google_results(results)
with open('frequency.csv', 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(freq_dict.items())


def select_words(freq_df, num_words_needed, max_char_freq):
    freq_df = freq_df.sample(frac=1)  # shuffle rows
    # freq_df = freq_df.sort_values(by=['freq'])
    char_counter = {letter: 0 for letter in letters}
    selected_words = {}
    for index, row in freq_df.iterrows():
        good_word = True
        # check char counts
        for char in row['word']:
            if char_counter[char] >= max_char_freq:
                good_word = False
                break
        if not good_word:
            continue
        # check similar selected words
        if not look_similar(row['word'], selected_words, strict=True):
            # add to selected words
            selected_words[row['word']] = (row['f1'] + row['f2'] + row['f3']) / 3
            if len(selected_words) > num_words_needed:
                break
            for char in row['word']:
                char_counter[char] += 1
    return selected_words, char_counter


freq_upper_limit = 10000000
freq_df = pd.read_csv('frequency.csv')
freq_df = freq_df.loc[(freq_df['f1'] <= freq_upper_limit) & (freq_df['f2'] <= freq_upper_limit) & (freq_df['f3'] <= freq_upper_limit)]
selected_words, char_counter = select_words(freq_df, 32, 6)
print(len(selected_words))
for char in char_counter:
    print('%s,%d' % (char, char_counter[char]))
for word in selected_words:
    print('%s,%d' % (word, selected_words[word]))
