# -*- coding: utf-8 -*-


import csv
from pprint import pprint
import random
import string
import re


def read_csv_data(file_to_read):
    '''read the csv file and return the list of dicts'''
    result = []
    with open(file_to_read) as f:
        reader = csv.DictReader(f)
        for row in reader:
            result.append(dict(row))
    return result


def write_csv_data(file_to_write,data):
    '''write a list of dicts to csv file'''
    keys = data[0].keys()
    with open(file_to_write,'w') as f:
        csv_writer = csv.DictWriter(f,keys)
        csv_writer.writeheader()
        csv_writer.writerows(data)


def dict_finder(web_site_name,list_dict):
    for data in list_dict:
       if data['name'].lower() == web_site_name.lower():
            return data
    raise TypeError('No data was found in the dict with the name: {web_site_name}')


def pw_gen(size = 12, chars=string.ascii_letters + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


