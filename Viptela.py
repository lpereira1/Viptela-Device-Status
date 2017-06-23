import requests
import json
import pprint

import credentials


session = requests.session()
payload = {"j_username":credentials.username, "j_password": credentials.password, 'submit': 'Log In'}
r = session.post(url='https://127.0.0.1:11443/j_security_check', data=payload, verify=False)


data = session.get(url='https://127.0.0.1:11443/dataservice/system/device/vedges/', verify=False)
serial = '11OG403170541'
for i in json.loads(data.text)['data']:
    #pprint.pprint(json.loads(data.text)['data'][i])
    if serial in i.values():
        try:
            responsedict = {'Device': serial,'Status': i['deviceState'],
                        'Operating Mode': i['configOperationMode'],
                        'systemip': i['system-ip']}
        except KeyError:
            responsedict = {'Device': serial, 'Status': i['deviceState'],
                            'Operating Mode': i['configOperationMode'],
                            'systemip': 'N/A'}
        print(responsedict)


if responsedict['systemip'] != 'N/A':
    colordata = session.get(url='https://' + '127.0.0.1:11443' +
                                '/dataservice/device/control/connections?deviceId=' + '172.21.186.77')
    countgold = 0
    countprivate1 = 0
    for i in json.loads(colordata.text)['data']:
        print(i)
        if 'gold' == i['local-color'] and 'up'== i['state']:
            countgold += 1
        elif 'private1' == i['local-color'] and 'up' == i['state']:
            countprivate1 += 1
        print(countgold)
        print(countprivate1)
else:
    countgold = 'N/A'
    countprivate1 = 'N/A'


    #print("not found")
#pprint.pprint(json.loads(data.text))