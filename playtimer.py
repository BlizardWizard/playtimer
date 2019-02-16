import configparser
import psutil
import time
import io


app_data = configparser.ConfigParser()
app_data.read('data.ini')

config = configparser.ConfigParser()
config.read('config.ini')
config = config['config']


if config['mode'] == 'blacklist':
    with io.open('blacklist.txt', 'r') as bypass_file:
        bypass = bypass_file.readlines()
        for item in bypass:
            bypass[bypass.index(item)] = item.replace('\n', '')
elif config['mode'] == 'whitelist':
    with io.open('whitelist.txt', 'r') as bypass_file:
        bypass = bypass_file.readlines()
        for item in bypass:
            bypass[bypass.index(item)] = item.replace('\n', '')


index = 0
for proc in psutil.process_iter():
    try:
        processName = str(proc.name())
        processID = proc.pid

        if config['mode'] == 'blacklist':
            bypassed = False
            if (processName in bypass):
                bypassed = True
                try:
                    app_data.remove_section(processName)
                except (configparser.NoSectionError):
                    pass
        elif config['mode'] == 'whitelist':
            bypassed = True
            if (processName in bypass):
                bypassed = False
                try:
                    app_data.remove_section(processName)
                except (configparser.NoSectionError):
                    pass

        if not bypassed:
            # app_data[processName] = {}
            # uncomment this line to jumnpstart app.ini file initialization ^^^
            app_data[processName]['index'] = str(index)
            app_data[processName]['ID'] = str(processID)
            playtime = str(app_data[processName].get('playtime', '0'))
            app_data[processName]['playtime'] = playtime
            index += 1
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass


with open('data.ini', 'w') as file:
    app_data.write(file)
    file.close()
