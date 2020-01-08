#!/home/python/venv/pyneng-py3/bin/python
# -*- coding: utf-8 -*-
''' Change password on websties and send new passwords to list of mails, as well writes them
into the file '''


import datetime
import logging
from web_scen import nic_web_change,masterhost_web_change
from data_proc import read_csv_data,write_csv_data,dict_finder,pw_gen
from mailer import msg_generator,send_mail
import logging
# IMPORT CONFIG VARIABLES
from config import PASS_FILE,LOG_FILE,from_addr,to_addr,subject,msg_subject



#Settings for a logging system in the programm
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
    )


def main():
    logging.info('Start the programm')
    #Create an empty message list
    msg = ['Nic and Masterhost monthly password change']
    
    
    # Read file with passwords
    logging.info(f'Reading the passwords form {PASS_FILE}')
    csv_current_creds = read_csv_data(PASS_FILE)
    nic_creds = dict_finder('nic',csv_current_creds)
    masterhost_creds = dict_finder('masterhost',csv_current_creds)
    logging.info(f"Read password from {PASS_FILE} and save them as dict, NIC: {nic_creds['password']}, MASTERHOST: {masterhost_creds['password']}")
    
    
    # Generate a new password
    new_pass = pw_gen()
    logging.info(f"Generate new NIC passwords {new_pass}")
    
    
    #Change a password on NIC
    if not nic_web_change(nic_creds['password'],new_pass,nic_creds['login']):
        logging.warning('Unable to change pass on NIC!!!')
        msg.append(f"NIC password was not changed and stayed the same: {nic_creds['password']}")
    else:
        #Save a new applied password in the dict
        nic_creds['password']=new_pass
        nic_creds['date'] = str(datetime.datetime.now()) 
        logging.info('New password has applied for NIC')
        msg.append(f"NIC has a new password: {new_pass}")
    
    
    #Change the password on MASTERHOST
    new_pass = pw_gen()
    logging.info(f"Generate new Masterhost passwords {new_pass}")
    #print(f"current pass : {masterhost_creds['password']}, new_pass: {new_pass} and login: {masterhost_creds['login']}")
    if not masterhost_web_change(masterhost_creds['password'],new_pass,masterhost_creds['login']):
        msg.append(f"Masterhost Password has not changed and stayed the same: {masterhost_creds['password']}")
        logging.warning('Unable to change pass on Masterhost!!!')
    else:
        masterhost_creds['date'] = str(datetime.datetime.now()) 
        masterhost_creds['password']=new_pass 
        logging.info('New password has applied for MASTERHOST')
        msg.append(f"Masterhost has a new password: {new_pass}")
    
    
    #Generate a new list of the dict for data    
    updated_creds = [masterhost_creds,nic_creds]    
    #Write a new passwords to the file
    write_csv_data(PASS_FILE,updated_creds)
    logging.info(f'Writing new password in {PASS_FILE}')
    #Send a new passwords to the mail
    send_mail(from_addr,to_addr,message_text = msg_generator(msg),subject=subject)
    logging.info(f'Sending a mail to {to_addr}')
    logging.info("End of the program")
        


if __name__=="__main__":
    main()
    
    





