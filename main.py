
from crypt import methods
from time import sleep
from flask import Flask, jsonify, render_template, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
import json
from wtforms.validators import InputRequired
from importlib.resources import path
import socket


IP = "127.0.0.1"
PORT = 10010
buffersize = 1024
format = "utf8"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static_old/files'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

def is_json(json_string):
  try:
    json.loads(json_string)
  except ValueError as e:
    return False
  return True

@app.route('/', methods=['GET',"POST"])

@app.route('/show',methods=['GET',"POST"])
def show():
    data_receive = request.json

    print("Success Receice !")

    with open("NewAppIP.json", 'r') as fp:
        AppData = json.load(fp)
    
    listObj = data_receive
    for flow_entry in  listObj['flows']['br-lan']:
        if flow_entry['detected_application_name'] in AppData:
            # print(flow_entry['detected_application_name'])
            if flow_entry['other_ip'] not in AppData[flow_entry['detected_application_name']]['ip_list']:
                print(flow_entry['other_ip'])
                new_ip_data_set = {flow_entry['other_ip']: flow_entry['other_port']}
                AppData[flow_entry['detected_application_name']]['ip_list'].update(new_ip_data_set)
            if "host_server_name" in flow_entry:
                if flow_entry['host_server_name'] not in AppData[flow_entry['detected_application_name']]['host_server_name'] :
                    print(flow_entry['host_server_name'])
                    AppData[flow_entry['detected_application_name']]['host_server_name'].append(flow_entry['host_server_name'])
        else:
            ip = { flow_entry['other_ip']: flow_entry['other_port']}
            if "host_server_name" in flow_entry:
                host = [flow_entry['host_server_name']]
            else:
                host = []
            new_data_set =  { flow_entry['detected_application_name'] : { "ip_list" : ip, "host_server_name" : host } }
            AppData.update(new_data_set)

    x_file_name = 'NewAppIP.json'
    with open(x_file_name, 'w') as json_file:
        str_rp = str(AppData)
        str_rp = str_rp.replace("'",'"')
        json_file.write(str_rp)

    return "Sussess Send !"

@app.route('/detected_protocol',methods=['GET',"POST"])
def detected_protocol():
    data_receive = request.json
    print("Receive ok")

    with open("detected_protocol_name.json", 'r') as fp:
        AppData = json.load(fp)

    listObj = data_receive
    Count = 0
    for flow_entry in  listObj['flows']['br-lan']:
        for i in range(0,len(flow_entry)):
            data_name = listObj['flows']['br-lan'][i]['detected_protocol_name']
            print(data_name)
            if data_name not in AppData:
                new_data_set = {data_name: {"number of appearances": 0}}
                AppData.update(new_data_set)
            else:
                Number_present = AppData[data_name]["number of appearances"]
                Count = Number_present + 1
                AppData.update({data_name:{"number of appearances": Count}})
    

    x_file_name = 'detected_protocol_name.json'
    with open(x_file_name, 'w') as json_file:
        str_rp = str(AppData)
        str_rp = str_rp.replace("'",'"')
        json_file.write(str_rp)

    return "Send ok !!!!"


@app.route('/show_detected_protocol',methods=['GET',"POST"])
def show_detected_protocol():
    with open('detected_protocol_name.json','r') as f:
        data = f.read()
    return render_template('detect_protocol.html',data = data)


@app.route('/Applications', methods=['GET',"POST"])
def Applications():
    with open('NewAppIP.json','r') as f:
        data = f.read()
    return render_template('Applications.html', data = data)


if __name__ == '__main__':
    app.run(debug=True)