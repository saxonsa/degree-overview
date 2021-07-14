from flask import Blueprint, request, jsonify
from models.user import User
from models.student import Student
from models.lecturer import Lecturer


# 注册蓝图
user = Blueprint("user", __name__)


@user.route('/vpntest', methods=['GET'])
def vpn_test():
    print(request.remote_addr)
    print(request.host)


@user.route('/login', methods=['POST'])
def login():
    """
    登录模块
    """
    print(request.remote_addr)
    print(request.host)

    # 登录所需参数
    user_id = request.args.get('userId')
    password = request.args.get('password')
    role = request.args.get('role')

    # 如果少参数
    if not all([user_id, password, role]):
        return jsonify({
            'code': 3001,
            'info': "Error! Missing parameters"
        }), 200

    user = None

    # 判断用户想要登录的身份并且检索用户
    if role == 'student':
        user = Student.query.filter_by(stuid=user_id).first()

    elif role == 'lecturer':
        user = Lecturer.query.filter_by(staffid=user_id).first()

    elif role == 'designer':
        user = Lecturer.query.filter_by(staffid=user_id).first()

    if user is None:
        return jsonify({
            'code': 3002,
            'info': 'No such user found, please check the username or the selected role'
        }), 200

    # 检查密码和登录
    if user.check_password(password):
        if role == 'student':
            token = User.generate_auth_token(user.stuid)
        else:
            token = User.generate_auth_token(user.staffid)

        response = {
            'code': 200,
            'info': 'success',
            'result': {
                'me': {
                    'id': user_id,
                    'engname': user.get_englishname(),
                    'nickname': user.get_nickname(),
                    'phone': user.get_phone(),
                    'email': user.get_email(),
                    'role': role,
                    'gender': user.get_gender(),
                    'program': user.get_program()
                },
                'token': token
            }
        }

        # 如果是lecturer, 添加designAuth字段
        if role == 'lecturer' or role == 'designer':
            response['result']['me']['designAuth'] = user.get_design_auth()

        return jsonify(response), 200
    # 密码错误
    else:
        response = {
            'code': 3003,
            'info': 'wrong password'
        }
        return jsonify(response), 200

