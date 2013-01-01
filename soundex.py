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
LEN1    = re.compile('^(.)$')
LEN2    = re.compile('^(..)$')
LEN3    = re.compile('^(...)$')
LENGT4  = re.compile('^(....).+$')

app = Flask(__name__)

def substitute(name):
    while True:
        if ONE.match(name):
            name = ONE.sub('\g<1>\g<2>1\g<4>', name, 1)
        elif TWO.match(name):
            name = TWO.sub('\g<1>\g<2>2\g<4>', name, 1)
        elif THREE.match(name):
            name = THREE.sub('\g<1>\g<2>3\g<4>', name, 1)
        elif FOUR.match(name):
            name = FOUR.sub('\g<1>\g<2>4\g<4>', name, 1)
        elif FIVE.match(name):
            name = FIVE.sub('\g<1>\g<2>5\g<4>', name, 1)
        elif SIX.match(name):
            name = SIX.sub('\g<1>\g<2>6\g<4>', name, 1)
        elif DOUBLE.match(name):
            name = DOUBLE.sub('\g<1>\g<2>\g<4>', name, 1)
        elif VOWEL.match(name):
            name = VOWEL.sub('\g<1>\g<2>\g<4>', name, 1)
        elif LEN1.match(name):
            name = LEN1.sub('\g<1>000', name, 1)
        elif LEN2.match(name):
            name = LEN2.sub('\g<1>00', name, 1)
        elif LEN3.match(name):
            name = LEN3.sub('\g<1>0', name, 1)
        elif LENGT4.match(name):
            name = LENGT4.sub('\g<1>', name, 1)
        else:
            break
    return name

def get_soundex(name):
    soundex = substitute(name)
    return name[0] + soundex[1:4]

@app.route('/encode', methods=['GET', 'POST'])
def soundex_encode():
    if request.method == 'POST':
        name = request.form['name'].upper()
        return render_template('encode.html', raw=name, soundex=get_soundex(name))
    return render_template('encode.html')

@app.route('/encode/<name>')
def url_encode(name):
    name = name.upper()
    response = json.dumps({ 'raw': name, 'soundex': get_soundex(name) })
    return Response(response, mimetype='application/json')

@app.route('/')
def spec():
    return render_template('spec.html')

if __name__ == '__main__':
    #Bind to PORT if defined, otherwise default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
