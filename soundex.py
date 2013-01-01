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
DBL1    = re.compile('^([BFPV])(1)(.*)$')
DBL2    = re.compile('^([CGJKQSXZ])(2)(.*)$')
DBL3    = re.compile('^([DT])(3)(.*)$')
DBL4    = re.compile('^([L])(4)(.*)$')
DBL5    = re.compile('^([MN])(5)(.*)$')
DBL6    = re.compile('^([R])(6)(.*)$')
LEN1    = re.compile('^(.)$')
LEN2    = re.compile('^(..)$')
LEN3    = re.compile('^(...)$')
LENGT4  = re.compile('^(....).+$')

app = Flask(__name__)

def encode(name):
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
        elif DBL1.match(name):
            name = DBL1.sub('\g<1>\g<3>', name, 1)
        elif DBL2.match(name):
            name = DBL2.sub('\g<1>\g<3>', name, 1)
        elif DBL3.match(name):
            name = DBL3.sub('\g<1>\g<3>', name, 1)
        elif DBL4.match(name):
            name = DBL4.sub('\g<1>\g<3>', name, 1)
        elif DBL5.match(name):
            name = DBL5.sub('\g<1>\g<3>', name, 1)
        elif DBL6.match(name):
            name = DBL6.sub('\g<1>\g<3>', name, 1)
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

@app.route('/encode', methods=['GET', 'POST'])
def soundex_encode():
    if request.method == 'POST':
        name = request.form['name'].upper()
        return render_template('encode.html', raw=name, soundex=encode(name))
    return render_template('encode.html')

@app.route('/encode/<name>')
def url_encode(name):
    name = name.upper()
    response = json.dumps({ 'raw': name, 'soundex': encode(name) })
    return Response(response, mimetype='application/json')

@app.route('/')
def spec():
    return render_template('spec.html')

if __name__ == '__main__':
    #Bind to PORT if defined, otherwise default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
