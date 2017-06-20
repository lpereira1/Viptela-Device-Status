import requests
import json
import pprint


session = requests.session()
payload = {"j_username":"verizon", "j_password": "Verizon123", 'submit': 'Log In'}
r = session.post(url='https://127.0.0.1:11443/j_security_check', data=payload, verify=False)


data = session.get(url='https://127.0.0.1:11443/dataservice/system/device/vedges/', verify=False)
serial = '11OD2143153190'
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
                                '/dataservice/device/control/connections?deviceId=' + '172.21.182.36')
    countgold = 0
    countprivate1 = 0
    for i in json.loads(colordata.text)['data']:
        print(i['local-color'])
        if 'gold' == i['local-color']:
            countgold += 1
        elif 'private1' == i['local-color']:
            countprivate1 += 1
        print(countgold)
        print(countprivate1)
else:
    countgold = 'N/A'
    countprivate1 = 'N/A'


    #print("not found")
#pprint.pprint(json.loads(data.text))