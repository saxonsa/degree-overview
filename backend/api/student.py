from flask import Blueprint, request, jsonify, abort
from models.student import Student
from models.base import db

student = Blueprint("student", __name__)


@student.route('/register', methods=['POST'])
def new_student():
    """
    Student 注册, 前端不提供此界面, 仅管理员添加 Student 时使用, 密码会在注册的时候进行加密 (sha256)
    """
    # 注册需要提供的参数如下
    stuid = request.args.get('stuid')
    password = request.args.get('password')
    nickname = request.args.get('nickname')
    englishname = request.args.get('englishname')
    gender = request.args.get('gender')
    phone = request.args.get('phone')
    email = request.args.get('email')
    program = request.args.get('program')
    register_year = request.args.get('register_year')

    # 检查参数可行性
    if stuid is None or password is None:
        abort(400) # missing compulsory arguments
    if Student.query.filter_by(stuid=stuid).first() is not None:
        abort(400) # existing user

    # 添加用户
    student = Student(nickname,password, englishname, phone, email, None, program, gender, stuid, register_year)
    db.session.add(student)
    db.session.commit()

    # 返回结果
    return jsonify({
        'code': "200",
        'info': 'register success',
        'result': 1
    }), 200
