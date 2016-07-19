from flask import (
    current_app as app,
    Blueprint,
    jsonify,
    request,
    render_template
)

root = Blueprint('root', __name__)


@root.route('/')
@root.route('/<path:path>')
def hello_world(path=""):
    msg = 'Hello World! Your path is "{0}" with args {1}'.format(
        path,
        str(request.args)
    )
    app.logger.info(msg)
    return msg


@root.route('/monitor')
def monitor():
    return '<body><h1>Monitor alive!</body>'


@root.route('/buggy')
def buggy():
    assert app.debug == False, "Don't panic! You're here by request of debug()"
    return "in production"


@root.route('/monitor/ping')
def ping():
    return jsonify(results=[])

@root.route('/monitor/version')
def version():
    return render_template('public/version.html')

@root.route('/config')
def config():
    msg = 'ZillowWebHostName in this environment is at http://{0}'
    msg = msg.format(app.config['ZillowWebHostName'])
    return msg
