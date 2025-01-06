# -*- coding: utf-8 -*-
import os 
import json 







def read_credential_file(service_name):
    try:
        filepath = os.environ['CREDENTIAL_PATH']
        if os.path.isfile(filepath): pass 
        else: raise
    except Exception as e:
        print([e, 'README.md 를 읽어보세요'])
        raise
    else:
        with open(filepath, mode='br') as f:
            d = json.loads(f.read())
            f.close()
        return d[service_name]
    

def read_credientials(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        d = json.loads(f.read())
        f.close()
    return d 
