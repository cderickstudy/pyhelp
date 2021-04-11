import os
from werkzeug.utils import secure_filename
from flask_cors import CORS
from flask import (
    Flask,
    json,
    flash,
    request,
    jsonify
)

UPLOAD_FOLDER = './mainfiles/'
ALLOWED_EXTENSIONS = {'txt', 'csv', 'xlsx'}
api = Flask(__name__)
api.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
api.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cors = CORS(api, resources={r"/processfile": {"origins": "http://localhost:3000"}})

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@api.route('/processfile', methods=['POST'])
def post_files():
    print(request.files)
    print(request.data)
    print(request)
    if 'file' not in request.files:
        raise InvalidUsage('No file attached', status_code=400)
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(api.config['UPLOAD_FOLDER'], filename))
        # Probably here you can import the file that you need and do the operation with this file.
        # File will be upload on the folder Mainfiles and return success true.
        return json.dumps({"success": True}), 201
    raise InvalidUsage('File type not allowed', status_code=400)

if __name__ == '__main__':
    api.run()
