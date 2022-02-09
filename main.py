import json
from process import xlsProcess

# Please Read ReadMe.md

#环境配置文件位置
filepath='config.json'

def read_json_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    if type(data) is str:
        return json.loads(data)
    return data

if __name__ == '__main__':
    data = read_json_from_file(filepath)
    Process = xlsProcess(data['cookies'], data['googleAuth'], data['xls_input'], data['xls_output'], data['try_count'], data['time_out'])
    Process.xlsWriteProcess()