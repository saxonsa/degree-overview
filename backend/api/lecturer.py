from flask import Blueprint, request, jsonify, abort
from models.base import db
from models.lecturer import Lecturer

lecturer = Blueprint("lecturer", __name__)


@lecturer.route('/register', methods=['POST'])
def new_lecturer():
    """
    Lecturer 注册, 前端不提供此界面, 仅管理员添加 Lecturer 时使用, 密码会在注册的时候进行加密 (sha256)
    """
    # 注册需要提供的参数如下
    staffid = request.args.get('staffid')
    password = request.args.get('password')
    nickname = request.args.get('nickname')
    englishname = request.args.get('englishname')
    gender = request.args.get('gender')
    phone = request.args.get('phone')
    email = request.args.get('email')
    program = request.args.get('program')
    designAuth = int(request.args.get('design_auth'))
    staffHonor = request.args.get('staff_honor')

    # 检查参数可行性
    if staffid is None or password is None:
        abort(400) # missing compulsory arguments
    if Lecturer.query.filter_by(staffid=staffid).first() is not None:
        abort(400) # existing user

    # 添加用户
    lecturer = Lecturer(nickname,password, englishname, phone, email, None, program, gender, staffid, designAuth, staffHonor)
    db.session.add(lecturer)
    db.session.commit()

    # 返回结果
    return jsonify({
        'code': "200",
        'info': 'register success',
        'result': 1
    })