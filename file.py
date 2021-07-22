#!/usr/bin/python3

import csv
import datetime
import requests
import operator

dict = {}

FILE_URL = "https://storage.googleapis.com/gwg-content/gic215/employees-with-date.csv"

def get_start_date():
    """Interactively get the start date to query for."""

    print()
    print('Getting the first start date to query for.')
    print()
    print('The date must be greater than Jan 1st, 2018')
    year = int(input('Enter a value for the year: '))
    month = int(input('Enter a value for the month: '))
    day = int(input('Enter a value for the day: '))
    print()

    return datetime.datetime(year, month, day)

start_date = get_start_date()

def get_file_lines(url):
    """Returns the lines contained in the file at the given URL"""

    # Download the file over the internet
    response = requests.get(url, stream=True)

    lines = []

    for line in response.iter_lines():
        lines.append(line.decode("UTF-8"))
    return lines

def get_same_or_newer():

    data = get_file_lines(FILE_URL)
    reader = csv.reader(data[1:])

    for row in reader:
        dict["{} {}".format (row[0], row[1])] = row[3]
    return dict
get_same_or_newer()

sorted_dict = sorted(dict.items(), key=operator.itemgetter(1))
i=0
for date in sorted_dict:
    q=datetime.datetime.strptime(date[1],'%Y-%m-%d')
    if q < start_date:
        i=i+1
        continue
    else:
        for name_date in sorted_dict[i:]:
            dateOk = datetime.datetime.strptime(name_date[1],'%Y-%m-%d')
            date_format = (datetime.datetime.strftime(dateOk,'%b %d, %Y'))
            print ("Started on {} {}".format(date_format, name_date[0]))
        break

