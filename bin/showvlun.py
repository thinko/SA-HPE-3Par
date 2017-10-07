#!/usr/bin/python

from hp3parclient import client, exceptions
import json

# for DNS fill in domain name, for IPs please leave DOMAIN blank ("")
# hostnames or IP addresses
SERVERS = ['3par1','3par2']
DOMAIN = 'example.com'
SSHPORT = 'port=22'
USERNAME = 'user'
PASSWORD = 'password'
COMMAND = 'showvlun'

CMD_WITH_ARGS = [COMMAND, '-a', '-showcols', 'Lun,VVName,HostName,VV_WWN,Port,Host_WWN']
 
for SERVER in SERVERS:
    if DOMAIN == "":
      SERVER_NAME = SERVER
    else:
      SERVER_NAME = SERVER + '.' + DOMAIN
    ssh_client = client.ssh.HP3PARSSHClient(SERVER_NAME, USERNAME, PASSWORD, SSHPORT)
 
    #logging in
    try:
        ssh_client.open()
    except:
        print 'Login Failed on 3PAR array: ' + SERVER
 
    #run the command
    CMD_RETURN = ssh_client.run(CMD_WITH_ARGS)
 
    #logging out
    ssh_client.close()
   
    CMD_RETURN.pop()
    CMD_RETURN.pop()
 
    HEADERS = CMD_RETURN.pop(0)
    HEADERS = HEADERS.split(',')
 
    for LINE in CMD_RETURN:
        LINE_LIST = LINE.split(',')
        DICTIONARY = dict(zip(HEADERS, LINE_LIST))
        DICTIONARY['array'] = SERVER
        DICTIONARY['Lun_id'] = DICTIONARY['Lun']
        DICTIONARY.pop('Lun')
        out = json.dumps(DICTIONARY)
        print out
