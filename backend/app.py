from flask import Flask, make_response
from flask_cors import CORS
from config import DebugMode
from models.base import db
from api.user import user
from api.grade import grade
from api.course import course
from api.cilo import cilo
from api.student import student
from api.lecturer import lecturer
from api.file import file
from api.assessment import assessment
from api.system import system

app = Flask(__name__)

CORS(app, supports_credentials=True, resources=r'/*')
@app.after_request
def after_request(resp):
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST,GET,DELETE,PUT,OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization, multipart/form-data'
    resp.headers['Access-Control-Expose-Headers'] = '*'
    resp.headers['Access-Control-Max-Age'] = 604800
    return resp


app.config.from_object(DebugMode)
db.init_app(app)
app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(grade, url_prefix="/grade")
app.register_blueprint(course, url_prefix="/course")
app.register_blueprint(cilo, url_prefix="/cilo")
app.register_blueprint(student, url_prefix="/student")
app.register_blueprint(lecturer, url_prefix="/lecturer")
app.register_blueprint(file, url_prefix="/file")
app.register_blueprint(assessment, url_prefix="/assessment")
app.register_blueprint(system, url_prefix="/system")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
