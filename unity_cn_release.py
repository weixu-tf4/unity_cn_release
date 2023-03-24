import sys
import urllib.request as request
import json
import time

from string import Template

# get http code
def get_http_code(url, major_ver):
    search_str = 'window.__props__ ='
    len_search_str = len(search_str)
    r = request.urlopen(url, data=None, timeout=10)
    http_text = r.read().decode('utf-8')
    start = http_text.index(search_str)
    end = http_text.index(';', start + len_search_str)
    #print(f'start {start} end {end}')
    data = http_text[start + len_search_str: end]
    # json
    json_data = json.loads(data)
    ver_list = json_data['data']['globalRelease']['releaseMap']['full'][major_ver]
    #print(json_data['data']['globalRelease']['releaseMap']['full'][major_ver])
    handle_ver_list(ver_list)

# parse unity version json data
def handle_ver_list(ver_list_data):
    template_win=''
    with open('template_win.txt', 'r') as fi:
        template_win = Template(fi.read())
    
    template_mac_x86=''
    with open('template_macos_x86.txt', 'r') as fi:
        template_mac_x86 = Template(fi.read())
    
    template_mac_arm=''
    with open('template_macos_arm.txt', 'r') as fi:
        template_mac_arm = Template(fi.read())

    for ver in ver_list_data:
        date_str = time.strftime('%Y-%m-%d', time.localtime(int(ver['created'])))
        data = {
            'hash': ver['chineseHash'],
            'version': ver['title']+ver['chinesePostfix'],
        }
        print(f'version: {ver["title"]} hash: {ver["chineseHash"]} date: {date_str}')
        print('  MacOS: ')
        print(f'  DownloadAssistant: {ver["downloadMac"]["unityInstaller"]}')
        # mac x86
        if ver['downloadMac']['unityEditorIntel'] :
            print(f'  Intel:')
            print(template_mac_x86.substitute(data))
        # mac arm
        if ver['downloadMac']['unityEditorAppleSilicon'] :
            print(f'  AppleSilicon:')
            print(template_mac_arm.substitute(data))
        # win
        print('  Windows: ')
        if ver['downloadWin']['unityInstaller'] :
            print(f'  DownloadAssistant: {ver["downloadWin"]["unityInstaller"]}')
        if ver['downloadWin']['unityEditor64'] :
            print(f'  Windows:')
            print(template_win.substitute(data))

if __name__ == '__main__':
    print(len(sys.argv))
    print(sys.argv)
    if len(sys.argv) < 2:
        print('parmaters error, need major version, like: 2021')
    else:
        major_ver = sys.argv[1]
        url = f'https://unity.cn/releases/full/{major_ver}'
        print('url:', url)
        get_http_code(url, major_ver)