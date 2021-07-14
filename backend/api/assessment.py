from flask import Blueprint, request, jsonify, Response
from models.base import db
from models.cilo import CILO
from models.file import File
import xlrd

assessment = Blueprint("assessment", __name__)


@assessment.route("/import_assessment", methods=['POST'])
def import_assessment():
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
    assessment_file_data = xlrd.open_workbook(file_contents=file_content)

    # sheet 1
    table = assessment_file_data.sheet_by_index(0)

    assessment_content = []
    # output each line
    # table.nrows获取该sheet中的有效行数

    assessment = {
        'method': '',
        'weight': '',
        'CILOs': ''
    }
    for row_num in range(1, table.nrows):
        assessment['method'] = table.row_values(row_num)[0]
        assessment['weight'] = table.row_values(row_num)[1]
        assessment['CILOs'] = table.row_values(row_num)[2]
        assessment_content.append(assessment)
        assessment = {
            'method': '',
            'weight': '',
            'CILOs': ''
        }

    return jsonify({
        'code': 200,
        'info': 'load successfully',
        'result': {
            'assessment_content': assessment_content
        }
    }), 200


@assessment.route("/get_assessment_template", methods=['GET'])
def get_assessment_template():
    """
        Download Assessment_template.xlsx from database
        :return: Binary stream of excel file
        """
    assessment_template = File.query.filter_by(name='Assessment_template.xlsx').first()
    file_data = assessment_template.content
    return Response(file_data, mimetype='application/vnd.ms-excel')
