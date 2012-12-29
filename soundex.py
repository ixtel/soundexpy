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

def remove_vowel(matchobj):
    string = matchobj.group(0)
    len = string.__len__()
    if len == 2:
        return string[0]
    elif re.compile('[hHwW]').match(string[1]):
        return string[0] + string[2]
    else:
        return string[0] + '@' + string[2]

def scrub_encoding(soundex, root):
    soundex = re.sub('@', '', soundex, 0)
    while soundex.__len__() < 4:
        soundex += '0'
    soundex = root + soundex[1:4]
    return soundex

def strip_doubles(name):
    return DBL_PATTERN.sub('\\1', name)

def substitute(name):
    while True:
        if VOW_PATTERN.search(name):
            name = VOW_PATTERN.sub(remove_vowel, name, 1)
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
    return name

@app.route('/encode/<name>')
def soundex_encode(name):
    root = name[0]
    soundex = substitute(name)
    soundex = strip_doubles(soundex)
    soundex = scrub_encoding(soundex, root)
    return json.dumps({'raw': name, 'soundex': soundex})

if __name__ == '__main__':
    #Bind to PORT if defined, otherwise default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
