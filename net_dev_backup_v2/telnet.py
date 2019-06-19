import telnetlib
import time
import logging


def telnet_show_command(username = None, password= None, secret = None, ip = None, device_type = None,command = 'None'):
    '''Connect to the cisco device(switch,asa) by telnet, send one command or list of commands and return the output of the command'''
    #if not username or not password or not secret or not device or device_type:
    #   raise ValueError('Please input all data in the function')
    terminal_command = None
    if device_type.lower() == 'switch':
       terminal_command = 'terminal length 0\n'
    elif device_type.lower() == 'asa':
        terminal_command = 'terminal pager 0\n'
    try:
        logging.info(f'Connecting to the following device: {ip}') 
        with telnetlib.Telnet(ip) as t:
            t.read_until(b'Username:')
            t.write(username.encode('utf-8') + b'\n')
        
            t.read_until(b'Password:')
            t.write(password.encode('utf-8') + b'\n')
            t.write(b'enable\n')
        
            t.read_until(b'Password:')
            t.write(secret.encode('utf-8') + b'\n')
            t.write(terminal_command.encode('utf-8'))
            if isinstance(command,list):
                for one_com in command:
                    t.write(one_com.encode('utf-8') + b'\n')
                    time.sleep(4)
            elif isinstance(command,str):
                t.write(command.encode('utf-8') + b'\n')
                time.sleep(4)
            else:
                raise TypeError('Unsupported type of the command variable')
            output = t.read_very_eager().decode('utf-8')
            return output
    except ConnectionRefusedError:
        logging.warning(f'Unnable to connect to the {ip}')
    except TimeoutError:
        logging.warning(f'Timeout error due to connect to {ip}')
    




