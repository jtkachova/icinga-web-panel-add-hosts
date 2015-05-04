# icinga-web-panel-add-hosts
web panel for adding new hosts to icinga configuration file

###Requirments

-Python

-pip

-Flask==0.10.1

-Flask-DebugToolbar==0.9.2

-Flask-WTF==0.10.0

###Installation

pip -r requirments.txt

##Run app

python app.py

Application starts on port 5000

##Configuration

By default icinga configuration files are:

/etc/icinga/objects/services.cfg

/etc/icinga/objects/hosts.cfg

If you want to change paths,you can edit config_file and host_file variable in app.py

Also if you use dedicated service.cfg file with predefined checks, you can use add_host_services function, in this case new host adds to default checks:CPU,LOAD,Disk_Space. By default this function commented. You can uncomment it if needed.

They should be predefined in commands.cfg and in services,cfg, you can change this in function add_host_services in app.py

###Usage

In 127.0.0.1:5000 you'll prompt to specify instance name, ip, contact group, default check command and notification interval, after submit new host definition will add to hosts file and specify default checks to host. After this icinga will reload.

This application should be run in the same server where icinga running.

