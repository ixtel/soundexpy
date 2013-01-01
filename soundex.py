import os
import re
import json
from flask import Flask, render_template, request, Response

VOWEL   = re.compile('(.)[AEIOUYHW](.?)')
ONE     = re.compile('(.)[BFPV]')
TWO     = re.compile('(.)[CGJKQSXZ]')
THREE   = re.compile('(.)[DT]')
FOUR    = re.compile('(.)[L]')
FIVE    = re.compile('(.)[MN]')
SIX     = re.compile('(.)[R]')
DBL1    = re.compile('11+')
DBL2    = re.compile('22+')
DBL3    = re.compile('33+')
DBL4    = re.compile('44+')
DBL5    = re.compile('55+')
DBL6    = re.compile('66+')
DBL1F   = re.compile('^([BFPV])1+(.*)$')
DBL2F   = re.compile('^([CGJKQSXZ])2+(.*)$')
DBL3F   = re.compile('^([DT])3+(.*)$')
DBL4F   = re.compile('^([L])4+(.*)$')
DBL5F   = re.compile('^([MN])5+(.*)$')
DBL6F   = re.compile('^([R])6+(.*)$')
LEN1    = re.compile('^(.)$')
LEN2    = re.compile('^(..)$')
LEN3    = re.compile('^(...)$')
LENGT4  = re.compile('^(....).+$')

app = Flask(__name__)

def encode(name):
    temp = ''
    while temp != name:
        temp = name
        name = ONE.sub('\g<1>1', name)
        name = TWO.sub('\g<1>2', name)
        name = THREE.sub('\g<1>3', name)
        name = FOUR.sub('\g<1>4', name)
        name = FIVE.sub('\g<1>5', name)
        name = SIX.sub('\g<1>6', name)

    name = DBL1.sub('1', name)
    name = DBL2.sub('2', name)
    name = DBL3.sub('3', name)
    name = DBL4.sub('4', name)
    name = DBL5.sub('5', name)
    name = DBL6.sub('6', name)
    name = DBL1F.sub('\g<1>\g<2>', name)
    name = DBL2F.sub('\g<1>\g<2>', name)
    name = DBL3F.sub('\g<1>\g<2>', name)
    name = DBL4F.sub('\g<1>\g<2>', name)
    name = DBL5F.sub('\g<1>\g<2>', name)
    name = DBL6F.sub('\g<1>\g<2>', name)
    
    temp = ''
    while temp != name:
        temp = name
        name = VOWEL.sub('\g<1>\g<2>', name)

    name = LEN1.sub('\g<1>000', name)
    name = LEN2.sub('\g<1>00', name)
    name = LEN3.sub('\g<1>0', name)
    name = LENGT4.sub('\g<1>', name)
    
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
