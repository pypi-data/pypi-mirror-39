import os
from flask import Flask, jsonify

from rox.server.flags.rox_flag import RoxFlag
from rox.server.rox_server import Rox
from rox.server.rox_options import RoxOptions


class Container:
    def __init__(self):
        self.first_flag = RoxFlag()


def rox_setup():
    os.environ['ROLLOUT_MODE'] = 'LOCAL'
    options = RoxOptions(dev_mode_key='6f66e1826dea3acd69abedec')
    Rox.register('test', con)
    Rox.setup('5ae089f994ea359740e9e788', options)


con = Container()
rox_setup()
app = Flask(__name__)


@app.route('/api/values')
def values():
    return jsonify(['value1', 'value2'])


@app.route('/api/values/<id>')
def value(id):
    if con.first_flag.is_enabled():
        return jsonify('value%s' % id)
    else:
        return jsonify('Eladddddd')


@app.route('/api/values', methods=['POST'])
def post_value():
    return ''


@app.route('/api/values/<id>', methods=['PUT'])
def put_value(id):
    return ''


@app.route('/api/values/<id>', methods=['DELETE'])
def delete_value(id):
    return ''
