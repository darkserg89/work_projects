#!/usr/local/bin/python3.6
# -*- coding: utf-8 -*-


''' This script connects to network devices by creds in device.yaml
and copy their configs to tftp server.'''


import datetime
from ssh_connect import send_show_command,ping_check_devices,multithread_send_show_command
from telnet import telnet_show_command
from file_process import parse_hostname,read_yml_file,write_to_file
from dir_conf import COMMAND,CREDS,CREDS_TELNET,BACKUP_PATH,LOG_FILE
import logging


#Commands to run on the network devices
#COMMAND = 'sh running-config'
#Files with loggins,passwords,etc to connect to the network devices
#CREDS = '/home/python/all_creds/net_dev_backup/cred/devices_ssh.yaml'
#CREDS_TELNET = '/home/python/all_creds/net_dev_backup/cred/devices_telnet.yaml'
#Path to save backup files 
#BACKUP_PATH = '/home/python/all_creds/net_dev_backup/backups/'


#Settings for a logging system in the programm
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
    )

    

def old_main():
    #Define the current date
    today = datetime.date.today()
    today = str(today.strftime('%d%m%Y'))
    #Read the yaml file with credentials for devices
    devices = read_yml_file(CREDS)
    # Run the script to connect to devices and save config files
    for device in devices:
        if ping_check(device['ip']):
            write_to_file(send_show_command(device,COMMAND),device['ip']+'-'+today+'.backup')

def ssh_main():
    #Define the current date
    today = datetime.date.today()
    today = str(today.strftime('%d%m%Y'))
    #Read the yaml file with credentials for devices
    devices = read_yml_file(CREDS)
    result = multithread_send_show_command(send_show_command,devices,COMMAND)
    for conf in result:
        if isinstance(conf,str):
            write_to_file(conf,BACKUP_PATH + parse_hostname(conf)+'-'+today+'.backup')
        else:
            logging.warning(f"The loaded config file of some device is empty, unable to write it")
            
def telnet_main():
    #Define the current date
    today = datetime.date.today()
    today = str(today.strftime('%d%m%Y'))
    #Read the yaml file with credentials for devices
    devices = read_yml_file(CREDS_TELNET)
    commands = ['show running-config','show version']
    result = []
    for device in devices:
        conf = telnet_show_command(command=commands,**device)
        if isinstance(conf,str):
            write_to_file(conf,BACKUP_PATH + parse_hostname(conf) +'-'+today+'.backup')
        else:
            logging.warning(f"The loaded config file of device {device['ip']} is empty, unable to write")
#        write_to_file(conf,CONF_PATH + device['ip']+'-'+today+'.backup')
        
def test_multitrade_telnet_main():
    #Define the current date
    today = datetime.date.today()
    today = str(today.strftime('%d%m%Y'))
    #Read the yaml file with credentials for devices
    devices = read_yml_file(CREDS_TELNET)
    result = multithread_send_show_command(telnet_show_command,devices,command=COMMAND)
    for conf in result:
        if isinstance(conf,str):
            write_to_file(conf,BACKUP_PATH + parse_hostname(conf)+'-'+today+'.backup')
    
        
        




if __name__ == '__main__':
    ssh_main()
    telnet_main()
    
