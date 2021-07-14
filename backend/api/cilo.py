from flask import Blueprint, request, jsonify, Response
from models.base import db
from models.cilo import CILO
from models.file import File
from .token_auth import auth
import xlrd

cilo = Blueprint("cilo", __name__)


@cilo.route("/add_cilo", methods=['POST'])
def add_cilo():
    if request.method == "POST":

        course_code = request.args.get('course_code')
        index = request.args.get('index')
        content = request.args.get('content')

        cilo = CILO(course_code=course_code, index=index, content=content)
        db.session.add(cilo)
        db.session.commit()

    else:
        return jsonify({
            "code": "405",
            "info": 'method of request is not post',
            "return": 1
        })

    return jsonify({
        "code": "200",
        'info': 'add cilo successfully',
        'return': 1
    })


@cilo.route("/modify_cilo", methods=['POST'])
def modify_cilo():

    if request.method == 'POST':
        # get parameters sent from user
        course_code = request.args.get('course_code')
        index = request.args.get('index')
        content = request.args.get('content')

        # modify cilo
        cilo = CILO.query.filter_by(course_code=course_code, index=index).first()
        cilo.content = content
        db.session.commit()


    else:
        return jsonify({
            "code": "405",
            "info": 'method of request is not post',
            "return": 1
        })
    return jsonify({
        "code": "200",
        "info": 'modify cilo successfully',
        "return": 1
    })

@cilo.route("/import_cilo", methods=['POST'])
def import_cilo():
    # 获取文件
    file_obj = request.files.get('file')
    if not file_obj:
        return jsonify({
            'code': 1001,
            'info': 'No file detected!'
        }), 200

    # 读取文件二进制流
    file_content = file_obj.read()

    # 转换成excel形式
    cilo_file_data = xlrd.open_workbook(file_contents=file_content)

    # sheet 1
    table = cilo_file_data.sheet_by_index(0)

    CILO_content = []
    # output each line
    # table.nrows获取该sheet中的有效行数
    for row_num in range(1, table.nrows):
        if table.row_values(row_num)[0] < 5 and table.row_values(row_num)[1]:
            CILO_content.append(table.row_values(row_num)[1])

    return jsonify({
        'code': 200,
        'info': 'load successfully',
        'result': {
            'cilo_content': CILO_content
        }
    }), 200



@cilo.route("/get_cilo_template", methods=['GET'])
def get_cilo_template():
    """
    Download CILO_template.xlsx from database
    :return: Binary stream of excel file
    """
    cilo_template = File.query.filter_by(name='CILO_template.xlsx').first()
    file_data = cilo_template.content
    return Response(file_data, mimetype='application/vnd.ms-excel')


@cilo.route("/get_course_cilo", methods=['GET'])
@auth.login_required
def get_course_cilo():
    """
    :return: 返回课程对应的token
    """
    course_code = request.args.get('courseCode')

    cilo_orm_list = CILO.query.filter_by(course_code=course_code).all()

    cilo_list = []

    for cilo_orm in cilo_orm_list:
        cilo_list.append({
            'index': cilo_orm.index,
            'content': cilo_orm.content
        })

    return jsonify({
        'code': 200,
        'info': 'query cilo content successfully',
        'result': cilo_list
    })


@cilo.route('get_specific_cilo_content_by_index', methods=['GET'])
@auth.login_required
def get_specific_cilo_by_index():
    course_code = request.args.get('course_code')
    cilo_index = request.args.get('cilo_index')

    cilo_orm = CILO.query.filter_by(course_code=course_code, index=cilo_index).first()

    return jsonify({
        'code': 200,
        'info': 'query specific cilo successfully',
        'result': cilo_orm.content
    })