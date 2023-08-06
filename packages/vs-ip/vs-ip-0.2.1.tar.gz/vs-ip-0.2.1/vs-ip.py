 #!/usr/bin/env python
from splinter import Browser
import time
import json
import os.path
import sys

def changeIp(vsIp='192.168.1.1', password=None):
    browser = Browser('firefox', headless=True, incognito=True)
    browser.visit('http://'+vsIp)
    try:
        while True:
            if browser.is_text_present('Inserisci la password della tua Vodafone Station Revolution'):
                if password == None:
                    password = input('Inserisci la password della tua Vodafone Station Revolution: ')
                browser.find_by_css('#login_Password').fill(password)
                password = None
                browser.find_by_css('#btn_login').click()
            else:
                break;
        if browser.is_text_present('Il tuo account è bloccato'):
            print('Password errata: '+browser.find_by_css('#login_infoText_blockedIT').first.value)
            browser.quit()
            quit()
        if browser.is_text_present('Stato & Supporto'):
            print('Login riuscito.')
        else:
            print('Login non riuscito. Prova vs-ip setup')
            browser.quit()
            quit()
        browser.visit('http://'+vsIp+'/main.cgi?page=app.html#cat=status-and-support_restart')
        time.sleep(2)
        ip = browser.find_by_css('#dsl_internet_WanIp').first.value
        print('IP in uso: '+ip)
        print('Provo a cambiare IP...')
        browser.find_by_css('#dsl_btn_reconnect').click()
        try:
            while True:
                if ip != browser.find_by_css('#dsl_internet_WanIp').first.value:
                    ip = browser.find_by_css('#dsl_internet_WanIp').first.value
                    if ip == 'Nessun indirizzo IP':
                        print('Attendere prego...')
                    else:
                        print('Nuovo IP: '+ip)
                        browser.quit()
                        quit()
                time.sleep(2)
        except:
            pass
    except KeyboardInterrupt:
        browser.quit()
        quit()

def readConf():
    try:
        file = open('conf.json', 'r')
        conf = file.read()
        file.close()
        return json.loads(conf)
    except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
        file = open('conf.json', 'w')
        file.write(json.dumps({"ip": "192.168.1.1", "password": ""}))
        file.close()
        return readConf()

def setupConf():
    conf = readConf()
    ip = input('Inserisci l\'ip della Vodafone Station Revolution ['+conf['ip']+']: ')
    password = input('Inserisci la password della Vodafone Station Revolution ['+conf['password']+']: ')
    if ip != '':
        conf['ip'] = ip
    if password != '':
        conf['password'] = password;
    file = open('conf.json', 'w')
    file.write(json.dumps(conf))
    file.close()
    print('Setup completato.')


if 'setup' in sys.argv:
    setupConf()
    quit()

if os.path.isfile('conf.json') == False:
    setupConf()

conf = readConf()
changeIp(conf['ip'], conf['password'])

#ci sucsiamo se cacata e mio primo softwharz col pitone ..cacata
#xo funzia

