# -*- coding: utf-8 -*-

import netmiko
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging



def send_show_command(device,command):
    ''' send command in show mode on cisco device, return string '''    
    result = None
    try:
        with netmiko.ConnectHandler(**device) as ssh:
            logging.info('Connecting to {} ---->'.format(device['ip']))
            ssh.enable()
            ssh.disable_paging(command='terminal length 0',delay_factor=1)
            result=ssh.send_command(command)
    except ValueError:
        logging.warning('Error has occured due to connection to device: {}'.format(device['ip']))
    except netmiko.ssh_exception.NetMikoAuthenticationException:
        logging.warning('Authentication issue during connecting to {}'.format(device['ip']))
    except netmiko.ssh_exception.NetMikoTimeoutException:
        logging.warning('Timeout to connect to device: {}'.format(device['ip']))
    return result
    

def ping_check(ip_address,visible = True):
    '''Check if ip alive or dead by ping and return True or False'''
    input_list = ['ping','-c','3','-n',ip_address]
    result_ping = subprocess.run(input_list,stdout=subprocess.DEVNULL,encoding='utf-8')
    if result_ping.returncode == 0:
        return True
    else:
        if visible:
            logging.info('The ip: {} is Unreachable'.format(ip_address))
        return False

def ping_check_devices(devices_list):
    ''' Return a list of avalible devices checked by ping '''
    result = []
    for device in devices_list:
        if ping_check(device['ip']):
            result.append(device)
    


def multithread_send_show_command(function,devices,command,number_threads = 6):
    '''Connect to a network devices by using multithreading'''
    all_results = []
    with ThreadPoolExecutor(max_workers = number_threads) as executor:
        future_ssh = [executor.submit(function,device,command) for device in devices]
        for f in as_completed(future_ssh):
                all_results.append(f.result())
    return all_results
