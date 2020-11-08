from subprocess import Popen, PIPE
from time import sleep

project_home="E:/backups/772020/desktop/CMS" #your's project directory

Popen(['start', 'cmd', '/k', 'cassandra'], shell=True) #running shell on cmd
sleep(15)
while 1: #checking cassandra is running or not
    a=Popen('nodetool status', stdin=PIPE, stdout=PIPE, shell=True)
    sleep(3)
    if b'Datacenter' == a.stdout.read()[:10]:
        sleep(3)
        break

Popen(['start', 'cmd', '/k', '%CASSANDRA_HOME%/bin/cqlsh.py'], shell=True) # then run cassandra shell
Popen(['start', 'cmd', '/k', 'workon dj & cd '+project_home+' & python manage.py runserver'], shell=True) #then run the django project
