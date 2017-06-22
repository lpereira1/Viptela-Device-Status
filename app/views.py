from flask import render_template, request, url_for
import requests
import json
from app import application


import credentials

@application.route('/')
@application.route('/index')
def index():
    return render_template('index.html', title='Device Status')



@application.route("/results", methods=['POST'])
def results():
    # specify the url
    session = requests.session()
    payload = {"j_username": credentials.username, "j_password": credentials.password, 'submit': 'Log In'}
    r = session.post(url='https://'+ credentials.server + '/j_security_check', data=payload, verify=False)
    url = session.get(url='https://' + credentials.server + '/dataservice/system/device/vedges/', verify=False)
    serial = request.form['serial']
    for i in json.loads(url.text)['data']:
        # pprint.pprint(json.loads(data.text)['data'][i])
        if serial in i.values():
            try:
                responsedict = {'Device': serial,
                            'Status': i['configStatusMessage'],
                            'statusdetail': i['configStatusMessageDetails'],
                            'operatingmode': i['configOperationMode'],
                            'systemip': i['system-ip']}
            except KeyError:
                responsedict = {'Device': serial,
                            'Status': i['configStatusMessage'],
                            'statusdetail': i['configStatusMessageDetails'],
                            'operatingmode': i['configOperationMode'],
                                'systemip': 'N/A'}

    try:
        responsedict

    except NameError:
        responsedict = {'Device': 'Not Found', 'Status': 'Not Found', 'operatingmode': 'Not Found'}

        return render_template('show-results.html',
                                   data=responsedict, gold='N/A', private1='N/A')
    countgold = 0
    countprivate1 = 0
    if responsedict['systemip'] != 'N/A':
        colordata = session.get(url='https://' + credentials.server +
                                    '/dataservice/device/control/connections?deviceId=' + responsedict['systemip'])
        print(colordata.text)

        for i in json.loads(colordata.text)['data']:
            print(i['local-color'])
            if 'gold' == i['local-color'] and 'up'== i['state']:
                countgold += 1
            elif 'private1' == i['local-color'] and 'up'== i['state']:
                countprivate1 += 1

    if countgold == 0:
        goldstatus = 'DOWN'

    if countgold > 0:
        goldstatus = 'UP'

    if countprivate1 == 0:
        private1status = 'DOWN'

    if countprivate1 > 0:
        private1status = 'UP'

    if responsedict['systemip'] == 'N/A':
        private1status = 'N/A'
        goldstatus='N/A'



    return render_template('show-results.html',
                           data=responsedict,gold=goldstatus,private1=private1status)


