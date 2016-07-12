# -*- coding: utf-8 -*-

import sys
import json
import datetime as dt
from flask import Flask, Response, render_template, jsonify
from webargs import fields, validate
from webargs.flaskparser import use_kwargs
from gevent.pywsgi import WSGIServer
from gevent import monkey
from IdentityCard import IdentityCard

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

monkey.patch_all()

app = Flask(__name__)
cls = IdentityCard()
cls.initialize_areas()

req_args = {
    'num': fields.Int(missing=1, validate=validate.Range(min=1, max=50)),
    'min': fields.Int(missing=0, validate=validate.Range(min=0, max=100)),
    'max': fields.Int(missing=100, validate=validate.Range(min=0, max=100)),
    'sex': fields.Int(missing=0, validate=validate.Range(min=0, max=2)),
    'year': fields.Int(validate=validate.Range(min=1900, max=dt.datetime.now().year)),
    'month': fields.Int(validate=validate.Range(min=1, max=12)),
    'day': fields.Int(validate=validate.Range(min=1, max=31))
}


@app.route('/api', methods=['GET'])
@use_kwargs(req_args)
def api_identidycard(num, min, max, sex, year, month, day):
    ret = cls.generator(num, min, max, sex, year, month, day)
    tmp = []
    for r in ret:
        tmp.append({'name': r[0], 'id': r[1], 'birthday': r[2], 'age': r[3], 'sex': r[4], 'address': r[5]})

    return Response(
        response=json.dumps(tmp if len(tmp) > 1 else tmp[0], ensure_ascii=False, indent=2),
        status=200,
        mimetype="application/json;charset=utf-8")


@app.route('/', methods=['GET'])
@use_kwargs(req_args)
def web_identidycard(num, min, max, sex, year, month, day):
    ret = cls.generator(num, min, max, sex, year, month, day)
    users = []
    for r in ret:
        users.append({'name': r[0], 'id': r[1], 'birthday': r[2], 'age': r[3], 'sex': r[4], 'address': r[5]})

    return render_template('index.html', users=users)


@app.errorhandler(422)
def handle_validation_error(err):
    exc = err.data['exc']
    return jsonify({'errors': exc.messages}), 422

if __name__ == '__main__':
    http = WSGIServer(('', 5000), app.wsgi_app)
    http.serve_forever()
