import os
import re
import json
from flask import Flask, render_template, request, Response

DOUBLE  = re.compile('(.*)(.)(\2)+(.*)')
VOWEL   = re.compile('(.)(.*)([AEIOUYHW])(.*)')
ONE     = re.compile('^(.)(.*)([BFPV])(.*)$')
TWO     = re.compile('^(.)(.*)([CGJKQSXZ])(.*)$')
THREE   = re.compile('^(.)(.*)([DT])(.*)$')
FOUR    = re.compile('^(.)(.*)([L])(.*)$')
FIVE    = re.compile('^(.)(.*)([MN])(.*)$')
SIX     = re.compile('^(.)(.*)([R])(.*)$')

app = Flask(__name__)

def remove_vowel(matchobj):
    matchstr = matchobj.group(0)
    if matchstr.__len__() == 2:
        return matchstr[0]
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
        if ONE.search(name):
            name = ONE.sub('\g<1>\g<2>1\g<4>', name, 1)
        elif TWO.search(name):
            name = TWO.sub('\g<1>\g<2>2\g<4>', name, 1)
        elif THREE.search(name):
            name = THREE.sub('\g<1>\g<2>3\g<4>', name, 1)
        elif FOUR.search(name):
            name = FOUR.sub('\g<1>\g<2>4\g<4>', name, 1)
        elif FIVE.search(name):
            name = FIVE.sub('\g<1>\g<2>5\g<4>', name, 1)
        elif SIX.search(name):
            name = SIX.sub('\g<1>\g<2>6\g<4>', name, 1)
        elif DOUBLE.search(name):
            name = DOUBLE.sub('\g<1>\g<2>\g<4>', name, 1)
        elif VOWEL.search(name):
            name = VOWEL.sub(remove_vowel, name, 1)
        else:
            break
    return name

def get_soundex(name):
    root = name[0]
    soundex = substitute(name)
    soundex = strip_doubles(soundex)
    soundex = scrub_encoding(soundex, root)
    return soundex

@app.route('/encode', methods=['GET', 'POST'])
def soundex_encode():
    if request.method == 'POST':
        name = request.form['name'].upper()
        return render_template('encode.html', raw=name, soundex=get_soundex(name))
    return render_template('encode.html')

@app.route('/encode/<name>')
def url_encode(name):
    name = name.upper()
    response = json.dumps({'raw': name, 'soundex': get_soundex(name)})
    return Response(response, mimetype='application/json')

@app.route('/')
def spec():
    return render_template('spec.html')

if __name__ == '__main__':
    #Bind to PORT if defined, otherwise default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
