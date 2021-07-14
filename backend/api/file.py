from flask import Blueprint, request, jsonify
from models.file import File
from models.base import db

file = Blueprint("file", __name__)


@file.route('/save_file_to_db', methods=['POST'])
def save_file_to_db():
    file_obj = request.files.get('file')
    file_content = file_obj.read()
    file_name = file_obj.filename

    file_data = File(name=file_name, content=file_content)
    db.session.add(file_data)
    db.session.commit()
    return jsonify({
        'code': 200,
        'info': file_name + 'added successfully'
    }), 200
