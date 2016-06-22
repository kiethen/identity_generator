# -*- coding: utf-8 -*-

import sys
import json
from flask import Flask, request, Response, render_template
from gevent.pywsgi import WSGIServer
from gevent import monkey
from IdentityCard import IdentityCard

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

monkey.patch_all()

app = Flask(__name__)


@app.route('/api', methods=['GET'])
def api_identidycard():
    for arg in request.args:
        try:
            if int(request.args.get(arg)) < 0:
                return "Invalid arguments."
        except ValueError:
            return "Invalid arguments."

    num = int(request.args.get('num', '1'))
    min = int(request.args.get('min', '0'))
    max = int(request.args.get('max', '100'))
    sex = int(request.args.get('sex', '0'))
    cls = IdentityCard(num, min, max, sex)
    ret = cls.generator()
    tmp = []
    for r in ret:
        tmp.append({'name': r[0], 'id': r[1], 'birthday': r[2], 'age': r[3], 'sex': r[4], 'address': r[5]})

    return Response(
        response=json.dumps(tmp, ensure_ascii=False, indent=2),
        status=200,
        mimetype="application/json;charset=utf-8")


@app.route('/', methods=['GET'])
def web_identidycard():
    for arg in request.args:
        try:
            if int(request.args.get(arg)) < 0:
                return "Invalid arguments."
        except ValueError:
            return "Invalid arguments."

    num = int(request.args.get('num', '1'))
    min = int(request.args.get('min', '0'))
    max = int(request.args.get('max', '100'))
    sex = int(request.args.get('sex', '0'))
    cls = IdentityCard(num, min, max, sex)
    ret = cls.generator()
    users = []
    for r in ret:
        users.append({'name': r[0], 'id': r[1], 'birthday': r[2], 'age': r[3], 'sex': r[4], 'address': r[5]})

    return render_template('index.html', users=users)

if __name__ == '__main__':
    http = WSGIServer(('', 5000), app.wsgi_app)
    http.serve_forever()
