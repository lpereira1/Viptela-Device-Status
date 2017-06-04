import requests
import json
import pprint


session = requests.session()
payload = {"j_username":"admin", "j_password": "admin", 'submit': 'Log In'}
r = session.post(url='https://192.168.250.230/j_security_check', data=payload, verify=False)


data = session.get(url='https://192.168.250.230/dataservice/system/device/vedges/', verify=False)
serial = '11OD2143152882'
print(json.loads(data.text)['data'])
for i in json.loads(data.text)['data']:
    #pprint.pprint(json.loads(data.text)['data'][i])
    if serial in i.values():
        responsedict = {'Device': serial,'Status': i['deviceState'], 'Operating Mode': i['configOperationMode']}
        print(responsedict)
    #print("not found")
#pprint.pprint(json.loads(data.text))