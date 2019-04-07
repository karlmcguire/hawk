#!/usr/bin/env python3

import csv

tickers = []

with open("../data/currencies.csv") as currencies:
    rows = csv.reader(currencies, delimiter = ",")
    for currency in rows:
        tickers.append(currency[0])

with open("officialmcaffee.csv") as data:
    reader = csv.reader(data, delimiter = ",")
    for tweet in reader:
        use = False
        for word in tweet[6].split():
            if word.upper() == word and len(word) > 3 and len(word) < 9:
                if word in tickers:
                    use = True
                    break
        if use == True: 
            tweet.insert(0, word)
            print(','.join(tweet))
