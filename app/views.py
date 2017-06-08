from flask import render_template, request, url_for
import requests
import json
from app import app


import credentials

@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html', title='Device Status')


@app.route("/results", methods=['POST'])
def results():
    # specify the url
    session = requests.session()
    payload = {"j_username": credentials.username, "j_password": credentials.password, 'submit': 'Log In'}
    r = session.post(url='https://'+ credentials.server + '/j_security_check', data=payload, verify=False)
    url = session.get(url='https://' + credentials.server + '/dataservice/system/device/vedges/', verify=False)
    print(r.url)
    #serial = '11OD2143152882'
    serial = request.form['serial']
    for i in json.loads(url.text)['data']:
        # pprint.pprint(json.loads(data.text)['data'][i])
        if serial in i.values():
            responsedict = {'Device': serial, 'Status': i['deviceState'], 'operatingmode': i['configOperationMode']}
        try:
            responsedict
        except NameError:
            responsedict = {'Device': 'Not Found', 'Status': 'Not Found', 'operatingmode': 'Not Found'}


    return render_template('show-results.html',
                           data=responsedict)