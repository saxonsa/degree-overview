from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask import abort, jsonify
from config import DebugMode

auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token: str) -> bool:
    """
    检查token
    :param token: 来自request header中的Authorization (自动检索Bearer, 获取后面的部分)
    :return: token is valid or not
    """
    s = Serializer(DebugMode.SECRET_KEY)
    try:
        data = s.loads(token)
    except BadSignature:
        print('token 不正确')
        abort(401)
    except SignatureExpired:
        print('token 过期')
        abort(401)
    return True
