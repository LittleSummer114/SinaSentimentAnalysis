import os
def ReadConf():
    input_f = open(os.path.abspath('../../static/conf/system.conf'))
    sen_list = input_f.readlines()
    for temp_sen in sen_list:
        if 'HostName=' in temp_sen:
            hostname = temp_sen.strip().split('=')[1]
        elif 'HostPort=' in temp_sen:
            hostport = temp_sen.strip().split('=')[1]
        elif 'UserName=' in temp_sen:
            username = temp_sen.strip().split('=')[1]
        elif 'Passwd=' in temp_sen:
            passwd = temp_sen.strip().split('=')[1]
        elif 'DBName=' in temp_sen:
            dbname = temp_sen.strip().split('=')[1]
    input_f.close()
    return hostname, hostport, username, passwd, dbname
