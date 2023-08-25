import psutil
import json

def check_process_running(process_name):
    process_name += '.exe'
    for process in psutil.process_iter(['name']):
        if process.info['name'] == process_name:
            
            return json.dumps({
                'process': process_name.replace('.exe', ''),
                'status': True
            })
    return json.dumps({
        'process': process_name.replace('.exe', ''),
        'status': False
    })