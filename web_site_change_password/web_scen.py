# -*- coding: utf-8 -*-

from webbot import Browser

def nic_web_change(current_pass,new_pass,user):
    id_tag = 'js flexbox flexboxlegacy no-touch history rgba multiplebgs backgroundsize borderradius boxshadow textshadow opacity cssanimations csscolumns cssgradients no-cssreflections csstransitions fontface generatedcontent applicationcache'
    web = Browser(showWindow=False)
    web.go_to('https://www.nic.ru/auth/login/')
    web.type('92414',into='Номер договора NIC-D')
    web.type(current_pass,into='Пароль')
    web.click('Войти')
    web.click('Изменить пароль')
    web.type(current_pass,id = id_tag, number=1)
    web.type(new_pass,id = id_tag, number=2)
    web.type(new_pass,id = id_tag, number=3)
    web.click('Изменить')
    if 'Пароль изменен' in web.get_page_source(): 
        return True
    else:
        #web.get_screenshot_as_file('/home/python/all_creds/web_site_changer/error_nic.png')
        return False
 

def masterhost_web_change(current_pass,new_pass,user):
    web = Browser(showWindow=False)
    web.go_to('https://cp.masterhost.ru/login')
    web.type(user,into = 'login')
    web.type(current_pass,into='password')
    web.click('Войти')
    web.go_to('https://cp.masterhost.ru/access/passwd')
    web.type(new_pass,id = 'pass')
    web.type(new_pass,id = 'repass')
    web.click(classname='form_submit')
#    web.get_screenshot_as_file('/home/python/test.png')
    if 'Пароль успешно изменен.' in web.get_page_source(): 
        return True
    else:
        #web.get_screenshot_as_file('/home/python/all_creds/web_site_changer/rror_masterhost.png')
        return False
