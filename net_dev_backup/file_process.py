# -*- coding: utf-8 -*-



import re
import yaml
import logging


def parse_hostname(output):
    '''Parse the hostname in the show run config and return string'''
    regexp = 'hostname\W+(\S+)'
    result = re.search(regexp,output).group(1)
    if not result:
        return 'unknown device'
    return result


def read_yml_file(file_to_read):
    ''' Read the yaml file and return the dict with cred of the devices '''
    result = None
    with open(file_to_read) as f:
        result = yaml.load(f)
    return result


def write_to_file(output,file_name):
    with open(file_name,'w') as f:
        logging.info('Writing a file to {}'.format(file_name))
        f.write(output)
