#!/home/python/venv/pyneng-py3/bin/python
# -*- coding: utf-8 -*-

'''
Script takes jinja teplates, settings from creds and generate config files for the phones

'''



from jinja2 import Environment, FileSystemLoader
import json
import sys
import os

#$ python cfg_gen.py templates/for.txt data_files/for.yml

file_name_template = 'cfg{}.xml'
PATH_FOR_CONFIGS = '/home/python/my_work/grandstream_generator/configs/'


def generate_cfg_from_template(path_to_template,path_to_yaml,**kwargs):
    '''generate configs to xml files with the name , which includes mac address of the phone'''
    VARS_FILE = path_to_yaml
    TEMPLATE_DIR, template = os.path.split(path_to_template)
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        **kwargs)
    template = env.get_template(template)
    phones = None
    with open(VARS_FILE) as f:
        try:
            phones = json.loads(f.read())
        except json.decoder.JSONDecodeError:
            print("There is an error in {}".format(VARS_FILE))   
    for phone in phones:
        try:
            result = template.render(phones[phone])
        except:
            continue
        PATH_WRITE =PATH_FOR_CONFIGS + file_name_template.format(phones[phone]['mac'])
        print('CREATING CONFIG ------> {}'.format(file_name_template.format(phones[phone]['mac'])))
        write_to_file(result,PATH_WRITE)
        

def write_to_file(output, file_name):
    ''' write data to file '''
    with open(file_name,'w') as f:
        f.write(output)
        
        
def main():
    generate_cfg_from_template('/home/python/my_work/grandstream_generator/templates/cfgGXP2170_treasury.xml','/home/python/my_work/grandstream_generator/creds/treasury.json',trim_blocks=True,lstrip_blocks=True) 
    
        

if __name__=='__main__':
    main()
