#!/usr/bin/env python3

import csv
from pathlib import Path

total = 0

with open("../data/currencies.csv") as data:
    reader = csv.reader(data, delimiter = ",")
    for currency in reader:
        filename = "file_" + currency[0] + ".csv"
        f = Path("../data/" + filename)
        if f.is_file():
            with open("../data/" + filename) as market:
                days = csv.reader(market, delimiter = ",")
                for day in days:
                    if day[6] != "-":
                        # show to total 
                        total = total + int(day[6])
                    break 

print(total)
