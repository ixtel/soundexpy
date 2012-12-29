import os
import re
import json
from flask import Flask

DOUBLE  = re.compile(r'(.)\1*')
VOWEL   = re.compile('.[aAeEiIoOuUyYhHwW].?')
ONE     = re.compile('[bBfFpPvV]')
TWO     = re.compile('[cCgGjJkKqQsSxXzZ]')
THREE   = re.compile('[dDtT]')
FOUR    = re.compile('[lL]')
FIVE    = re.compile('[mMnN]')
SIX     = re.compile('[rR]')

app = Flask(__name__)

def remove_vowel(matchobj):
    matchstr = matchobj.group(0)
    if matchstr.__len__() == 2:
        return matchstr[0]
    elif re.compile('[hHwW]').match(matchstr[1]):
        return matchstr[0] + matchstr[2]
    else:
        return matchstr[0] + '@' + matchstr[2]

def scrub_encoding(soundex, root):
    soundex = re.sub('@', '', soundex, 0)
    while soundex.__len__() < 4:
        soundex += '0'
    soundex = root + soundex[1:4]
    return soundex

def strip_doubles(name):
    return DOUBLE.sub('\\1', name)

def substitute(name):
    while True:
        if VOWEL.search(name):
            name = VOWEL.sub(remove_vowel, name, 1)
        elif ONE.search(name):
            name = ONE.sub('1', name, 1)
        elif TWO.search(name):
            name = TWO.sub('2', name, 1)
        elif THREE.search(name):
            name = THREE.sub('3', name, 1)
        elif FOUR.search(name):
            name = FOUR.sub('4', name, 1)
        elif FIVE.search(name):
            name = FIVE.sub('5', name, 1)
        elif SIX.search(name):
            name = SIX.sub('6', name, 1)
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
