import os
import re
import json
from flask import Flask

DBL_PATTERN = re.compile(r'(.)\1*')
VOW_PATTERN = re.compile('.[aAeEiIoOuUyYhHwW].?')
BFPV     = re.compile('[bBfFpPvV]')
CGJKQSXZ = re.compile('[cCgGjJkKqQsSxXzZ]')
DT       = re.compile('[dDtT]')
L        = re.compile('[lL]')
MN       = re.compile('[mMnN]')
R        = re.compile('[rR]')

app = Flask(__name__)

def subvowel(matchobj):
    string = matchobj.group(0)
    len = string.__len__()
    if len == 2:
        return string[0]
    elif re.compile('[hHwW]').match(string[1]):
        return string[0] + string[2]
    else:
        return string[0] + '@' + string[2]

def strip_doubles(name):
    return DBL_PATTERN.sub('\\1', name)

@app.route('/encode/<name>')
def soundex_encode(name):
    #name = strip_doubles(name)
    raw = name
    root = name[0]
    while True:
        if VOW_PATTERN.search(name):
            name = VOW_PATTERN.sub(subvowel, name, 1)
        elif BFPV.search(name):
            name = BFPV.sub('1', name, 1)
        elif CGJKQSXZ.search(name):
            name = CGJKQSXZ.sub('2', name, 1)
        elif DT.search(name):
            name = DT.sub('3', name, 1)
        elif L.search(name):
            name = L.sub('4', name, 1)
        elif MN.search(name):
            name = MN.sub('5', name, 1)
        elif R.search(name):
            name = R.sub('6', name, 1)
        else:
            break
    name = strip_doubles(name)
    name = re.sub('@', '', name, 0)
    while name.__len__() < 4:
        name += '0'
    name = root + name[1:4]
    return json.dumps({'raw': raw, 'encoded': name})

if __name__ == '__main__':
    #Bind to PORT if defined, otherwise default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
