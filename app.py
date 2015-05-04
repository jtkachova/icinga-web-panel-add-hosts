from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_debugtoolbar import DebugToolbarExtension
import os
import cgi
import re
import subprocess
import shutil
from functools import wraps
from wtforms import Form, BooleanField, TextField, PasswordField, validators, TextAreaField
app = Flask(__name__)
app.secret_key = 'key'
config_file = "/etc/icinga/objects/services.cfg"
host_file = "/etc/icinga/objects/hosts.cfg"
tmp_file = "/tmp/icinga_test.cfg"
WTF_CSRF_SECRET_KEY = 'this-is-not-random-but-it-should-be'

def generate_host_definition(ip,instance_name,contact_group, check_command, notification_interval):
			string = 'define host{' + '\n   '  + \
                  'hostname             ' + instance_name + '\n   ' + \
				  'alias                ' + instance_name + '\n   ' + \
				  'address              ' + ip + '\n   '\
				  'max_check_attempts   5\n   '\
				  'contact_groups       ' + contact_group + '\n   ' + \
				  'check_command        ' + check_command + '\n   ' +  \
                  'notification interval ' + notification_interval + '\n ' + '}\n'
			return string
def add_host_definition(host_file,string):
			f1 = open(host_file, "a")
			f1.write(string)
			f1.close
def add_host_services(config_file,tmp_file,instance_name,arg1='CPU',arg2='LOAD',arg3='Disk_Space'):
			f1 = open(config_file, "r")
		  	f2 = open(tmp_file, "w")
			arg_list = [ arg1, arg2, arg3]
			counter = 0
			lines = f1.read().splitlines()
			for line in lines:
				for arg in arg_list:
					pattern = re.findall(arg, line)
					if pattern:
						position = [counter-1]
						prev_line = lines[counter-1]
						lines[counter-1] =  prev_line + ',' + instance_name
				counter += 1
			text = '\n'.join(lines)
			f2.write(text)
			f2.close
			f1.close
			shutil.copy2(tmp_file, config_file)
class ValidationForm(Form):
    ip = TextAreaField('ip', [validators.InputRequired()])
    instance_name = TextAreaField('instance name', [validators.InputRequired()])
    check_command = TextAreaField('check command', [validators.InputRequired()], description=('check_ssh'))
    contact_group = TextAreaField('contact group',[validators.InputRequired()], description=('admins'))
    notification_interval = TextAreaField('notification interval',[validators.InputRequired()], description=('1'))


@app.route('/', methods=['GET', 'POST'])
def welcome():
    error = None

    form = ValidationForm(request.form)
    subprocess.os.environ['config_file'] = config_file
    if request.method == 'POST'  and form.validate():
        ip = form.ip.data
        instance_name = form.instance_name.data
        check_command = form.check_command.data
        contact_group = form.contact_group.data
        notification_interval = form.notification_interval.data
        string = generate_host_definition(ip,instance_name,contact_group, check_command, notification_interval)
        add_host_definition(host_file,string)
        #Uncomment this function if you use dedicated services.cfg file
        #add_host_services(config_file,tmp_file,instance_name)
        rel = subprocess.Popen("/etc/init.d/icinga reload|echo $?", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = rel.communicate()
        template = output[0]
        template =''.join(template)
        template = template.strip()
        res = re.findall('0', template)
        if res:
                flash("ok")
        else:
                flash("adding to config failed. Please check your syntax")


    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=5000)
