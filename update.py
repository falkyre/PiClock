import os
import re
import sys

print('Updating Python Modules')
print('Updating python-dateutil')
os.system('sudo pip3 install python-dateutil --upgrade')
print('Updating tzlocal')
os.system('sudo pip3 install tzlocal --upgrade')
print('Updating python-metar')
os.system('sudo pip3 install python-metar --upgrade')

buttonFileName = 'Button/gpio-keys'
print('Checking ' + buttonFileName)
if os.path.isfile(buttonFileName):
    try:
        print('Setting proper permissions on ' + buttonFileName)
        os.chmod(buttonFileName, 0o744)
    except AttributeError:
        pass

apikeysFileName = 'Clock/ApiKeys.py'
wuapi_re = re.compile('\\s*wuapi\\s*=')
dsapi_re = re.compile('\\s*dsapi\\s*=')
ccapi_re = re.compile('\\s*ccapi\\s*=')
tmapi_re = re.compile('\\s*tmapi\\s*=')
owmapi_re = re.compile('\\s*owmapi\\s*=')

print('Checking ' + apikeysFileName)
if os.path.isfile(apikeysFileName):
    altered = False
    foundtm = False
    foundowm = False
    newfile = ''
    apikeys = open(apikeysFileName, 'r')
    for aline in apikeys:
        if tmapi_re.match(aline):
            foundtm = True
        if owmapi_re.match(aline):
            foundowm = True
        if wuapi_re.match(aline):
            print('Removing wuapi key from ' + apikeysFileName)
            altered = True
        if dsapi_re.match(aline):
            print('Removing dsapi key from ' + apikeysFileName)
            altered = True
        if ccapi_re.match(aline):
            print('Removing ccapi key from ' + apikeysFileName)
            altered = True
        else:
            newfile += aline
    apikeys.close()

    if not foundtm and not foundowm:
        print('This version of PiClock requires an OpenWeather One Call API 3.0 key.')
        print('https://home.openweathermap.org/subscriptions/unauth_subscribe/onecall_30/base')
        print('Enter your OpenWeather API key.')
        print('key: '),
        k = sys.stdin.readline()
        k = k.strip()
        if len(k) > 1:
            newfile += 'owmapi = \'' + k + '\''
            altered = True

    if altered:
        print('Writing Updated ' + apikeysFileName)
        apikeys = open(apikeysFileName, 'w')
        apikeys.write(newfile)
        apikeys.close()
    else:
        print('No changes made to ' + apikeysFileName)

    try:
        from rpi_ws281x import *  # NOQA
    except AttributeError:
        print('NeoAmbi.py now uses rpi-ws281x/rpi-ws281x-python')
        print('Please install it as follows:')
        print('sudo pip3 install rpi_ws281x')
