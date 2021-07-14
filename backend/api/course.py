from flask import Blueprint, request, jsonify
from models.course import Course
from models.cilo import CILO
from models.pre import Pre
from models.assessment import Assessment
from models.base import db
from models.lecturer import Lecturer
from .token_auth import auth
from .designer import check_designer_authority
from .log import write_txt_file
import time
import json
from sqlalchemy import and_

course = Blueprint("course", __name__)


@course.route("/create_course", methods=['POST'])
@auth.login_required
def create_course():

    staffid = request.args.get('staffid')
    course_name = request.args.get('courseName')
    course_code = request.args.get('courseCode')
    course_type = request.args.get('courseType')
    course_unit = request.args.get('courseUnit')
    course_program = request.args.get('courseProgram')
    academic_year = request.args.get('academicYear')
    cilo_content = request.args.getlist('CILO[]')
    assessment_list = request.args.getlist('assessment[]')
    pre_relation = request.args.getlist('preRelation[]')

    isDesigner = check_designer_authority(staffid)

    if isDesigner is True:
        # 创建课程
        new_course = Course(course_code=course_code, course_name=course_name, course_type=course_type,
                            department=course_program, unit=course_unit, year=academic_year)
        db.session.add(new_course)

        # 因为CILO和assessment后面很多都是基于course code做的foreign key, 所以必须先要有课程, 此处要先在course创建好后commit
        db.session.commit()

        # 添加CILO
        index = 0
        for cilo in cilo_content:
            index += 1
            new_cilo = CILO(course_code=course_code, index=index, content=cilo)
            db.session.add(new_cilo)
            # db.session.commit()

        # 添加assessment
        for assessment in assessment_list:
            assessment = eval(assessment)
            new_assessment = Assessment(course_code=course_code, method=assessment['method'],
                                        percentage=assessment['weight'], cilostr=assessment['CILOs'],
                                        year=academic_year)
            db.session.add(new_assessment)
            # db.session.commit()

        # 添加pre关系
        type = 0
        for pre in pre_relation:
            pre = eval(pre)
            type += 1
            for or_pre in pre:
                pre_exist_test = Pre.query.filter_by(post_course=course_code, post_cilo_index=int(or_pre['currentCILOIndex']),
                              pre_course=or_pre['courseCode'], pre_cilo_index=int(or_pre['CILOIndex']), type=type).first()

                if pre_exist_test is None:

                    new_pre = Pre(post_course=course_code, post_cilo_index=int(or_pre['currentCILOIndex']),
                                  pre_course=or_pre['courseCode'], pre_cilo_index=int(or_pre['CILOIndex']), type=type)
                    db.session.add(new_pre)
                    # db.session.commit()

        # update log ---------------------------------------------------------------------------------------- |

        # 写入基本信息
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        operation = 'Create course'

        course_basic = '\tcourse name: {};\n \tcode: {};\n \ttype: {};\n \tunit: {};\n \tbelonging program: {};\n' \
                           '\tstart year: {};\n'.format(
            course_name, course_code, course_type, course_unit, course_program, academic_year)

        basic_information = '[' + current_time + ']\n' + 'opeartion: ' + operation + '\ncourse basic information' \
                                                                                    ': \n' + course_basic
        write_txt_file(course_code, course_name, course_program, basic_information)

        # 写入 CILO
        write_txt_file(course_code, course_name, course_program, 'CILO information: \n')
        index = 0
        for cilo in cilo_content:
            index += 1
            write_txt_file(course_code, course_name, course_program, '\tCILO' + str(index) + ': ' + cilo + '\n')

        # 写入 Assessment
        write_txt_file(course_code, course_name, course_program, 'Assessment Information: \n')
        write_txt_file(course_code, course_name, course_program, '\tstart year to use: ' + str(academic_year) + '\n')
        for assessment in assessment_list:
            assessment = eval(assessment)
            weight = float(assessment['weight']) * 100
            write_txt_file(course_code, course_name, course_program, '\tmethod: ' + str(assessment['method']) + '; weight:' +
                            str(weight) + '%; Corresponding CILOs ' + str(assessment['CILOs']) + ';\n')

        # 写入 designer 信息
        write_txt_file(course_code, course_name, course_program, 'Designer information: \n')
        write_txt_file(course_code, course_name, course_program, '\tDesigner id: ' + staffid + '\n')
        designer = Lecturer.query.filter_by(staffid=staffid).first()
        write_txt_file(course_code, course_name, course_program, '\tname: ' + designer.get_nickname() + '(' +
                       designer.get_englishname() + ') ' + '\n')
        write_txt_file(course_code, course_name, course_program, '\tphone number: ' + designer.get_phone() + '\n')
        write_txt_file(course_code, course_name, course_program, '\temail: ' + designer.get_email() + '\n\n\n\n')

        # --------------------------------------------------------------------------------------------------- |

        # 全部成功后, 将数据库 commit 确定保存
        db.session.commit()

        return jsonify({
            'code': 200,
            'info': 'course created!',
        }),200

    else:
        pass


@course.route("/modify_course", methods=['PUT'])
@auth.login_required
def modify_course():
    staffid = request.args.get('staffid')
    course_code = request.args.get('courseCode')
    course_name = request.args.get('courseName')
    course_type = request.args.get('courseType')
    course_unit = request.args.get('courseUnit')
    course_department = request.args.get('courseDepartment')
    course_academic_year = request.args.get('courseAcademicYear')
    course_cilo = request.args.getlist('courseCILO[]')
    course_assessment = request.args.getlist('courseAssessment[]')

    isDesigner = check_designer_authority(staffid)

    if isDesigner is False:
        return jsonify({
            'code': 403,
            'info': 'You have no authorization to modify course',
            'result': 0
        })

    # 查看哪些信息被修改的flag
    type_flag = False
    unit_flag = False
    academic_year_flag = False
    cilo_flag = False
    assessment_flag = False
    new_assessment_flag = False

    # 验证参数合理性 ---------------------------------------------------

    # 修改数据 --------------------------------------------------------
    # 修改课程基本信息
    course_orm = Course.query.filter_by(course_code=course_code).first()
    if course_orm.course_type != course_type:
        course_orm.course_type = course_type
        type_flag = True
    if course_orm.unit != int(course_unit, 10):
        course_orm.unit = int(course_unit, 10)
        unit_flag = True
    if course_orm.year != course_academic_year:
        course_orm.year = course_academic_year
        academic_year_flag = True

    # 修改课程的CILO
    index = 0
    for cilo_str in course_cilo:
        index += 1
        # 这个for循环会跑 len(course_cilo) 次
        cilo_obj = eval(cilo_str)
        cilo_orm = CILO.query.filter_by(course_code=course_code, index=index).first()
        if cilo_orm.content != cilo_obj['content']:
            cilo_orm.content = cilo_obj['content']
            cilo_flag = True

    # 查看当前year的assessment有没有
    ass_year_orm = Assessment.query.filter_by(course_code=course_code, year=course_academic_year).first()
    if ass_year_orm is None:
        # 如果没有, 全部进行创建
        new_assessment_flag = True
        for assessment_str in course_assessment:
            assessment_obj = json.loads(assessment_str)
            new_assessment = Assessment(course_code=course_code, method=assessment_obj['method'],
                                        percentage=assessment_obj['weight'], cilostr=assessment_obj['cilostr'],
                                        year=course_academic_year)
            db.session.add(new_assessment)

    else:
        # 如果有, 进行修改
        # 删除已经在前端删掉的assessment
        delete_flag = True  # 设置是否需要删除的flag
        assessment_orm_list = Assessment.query.filter_by(course_code=course_code).all()
        for ass_orm in assessment_orm_list:
            for ass_str in course_assessment:
                ass_obj = json.loads(ass_str)
                if ass_obj['method'] == ass_orm.method:
                    # 如果找到了一样的method, 说明这个没有删掉
                    delete_flag = False
                    break
                delete_flag = True
            # 如果没有找到, 将其删掉
            if delete_flag is True:
                db.session.delete(ass_orm)
                assessment_flag = True

        # 修改课程的assessment
        for assessment_str in course_assessment:
            assessment_obj = json.loads(assessment_str)
            # print(type(assessment_obj['method']))
            assessment_orm = Assessment.query.filter(
                and_(Assessment.course_code==course_code, Assessment.method==assessment_obj['method'])
            ).first()
            # print(assessment_orm)
            if assessment_orm is not None:
                # 如果method存在, 进行修改
                if assessment_orm.percentage != assessment_obj['weight']:
                    assessment_orm.percentage = assessment_obj['weight']
                    assessment_flag = True
                if assessment_orm.cilostr != assessment_obj['cilostr']:
                    assessment_orm.cilostr = assessment_obj['cilostr']
                    assessment_flag = True
            else:
                # 如果method不存在就添加一个新的Assessment
                new_assessment = Assessment(course_code=course_code, method=assessment_obj['method'],
                                            percentage=assessment_obj['weight'],
                                            cilostr=assessment_obj['cilostr'], year=course_academic_year)
                db.session.add(new_assessment)
                assessment_flag = True

    db.session.commit()

    # update log for modify course ------------------------------------------------------------
    if type_flag or unit_flag or academic_year_flag or \
            cilo_flag or assessment_flag or new_assessment_flag:

        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        operation = 'Modify course'
        write_txt_file(course_code, course_name, course_department, '[' + current_time + ']\nOpeartion: '
                       + operation + '\n')
        write_txt_file(course_code, course_name, course_department, 'Changed information: \n')
        if type_flag is True:
            write_txt_file(course_code, course_name, course_department, '\tNew type: ' + course_type + '\n')
        if unit_flag is True:
            write_txt_file(course_code, course_name, course_department, '\tNew unit: ' + course_unit + '\n')
        if cilo_flag is True:
            write_txt_file(course_code, course_name, course_department, '\tNew CILO: ' + '\n')
            index = 0
            for cilo_str in course_cilo:
                cilo_obj = eval(cilo_str)
                write_txt_file(course_code, course_name, course_department, '\t\t' + str(index) + ': '
                               + cilo_obj['content'] + '\n')
                index += 1
        if new_assessment_flag is True:
            write_txt_file(course_code, course_name, course_department, '\tNew assessment for year '
                           + course_academic_year + ':\n')
            for ass_orm in course_assessment:
                ass_org = json.loads(ass_orm)
                weight = float(ass_org['weight']) * 100
                write_txt_file(course_code, course_name, course_department, '\t\tMethod: ' +
                               str(ass_org['method']) + '\tWeight: ' + str(weight) + '%\tCorresponding CILO: ' +
                               str(ass_org['cilostr']) + '\n')
        if assessment_flag is True:
            write_txt_file(course_code, course_name, course_department, '\tUpdated assessment: \n')
            for ass_orm in course_assessment:
                ass_org = json.loads(ass_orm)
                weight = float(ass_org['weight']) * 100
                write_txt_file(course_code, course_name, course_department, '\t\tMethod: ' +
                               str(ass_org['method']) + '\tWeight: ' + str(weight) + '%\tCorresponding CILO: ' +
                               str(ass_org['cilostr']) + '\n')
        write_txt_file(course_code, course_name, course_department, 'Designer information: \n')
        write_txt_file(course_code, course_name, course_department, '\tDesigner id: ' + staffid + '\n')
        designer = Lecturer.query.filter_by(staffid=staffid).first()
        write_txt_file(course_code, course_name, course_department, '\tname: ' + designer.get_nickname() + '(' +
                       designer.get_englishname() + ') ' + '\n')
        write_txt_file(course_code, course_name, course_department, '\tphone number: ' + designer.get_phone() + '\n')
        write_txt_file(course_code, course_name, course_department, '\temail: ' + designer.get_email() + '\n\n\n\n')

    else:
        return jsonify({
            'code': 200,
            'info': 'Nothing has been changed',
            'result': 1
        })

    return jsonify({
        'code': 200,
        'info': 'modify successfully',
        'result': 1
    })



@course.route("/get_course_detail_by_course_code", methods=['GET'])
@auth.login_required
def get_course_detail_by_course_code():

    course_code = request.args.get('courseCode')
    request_year = request.args.get('requestYear')

    # 获取课程信息
    course_orm = Course.query.filter_by(course_code=course_code).first()

    course = {
        'code': course_orm.course_code,
        'name': course_orm.course_name,
        'type': course_orm.course_type,
        'unit': course_orm.unit,
        'department': course_orm.department,
        'academic_year': course_orm.year,
        'CILO': [],
        'assessment': [],
        'prerequisite_relation': [],
        'prerequisite_course': [],
        'post_relation': [],
        'post_courses': []
    }

    # 获取CILO信息
    cilo_orm = CILO.query.filter_by(course_code=course_code).all()

    for cilo in cilo_orm:
        course['CILO'].append({
            'index': cilo.index,
            'content': cilo.content
        })

    if request_year is not None:
        # 如果传入了请求年份
        assessment_orm_list = Assessment.query.filter_by(course_code=course_code, year=request_year).all()
    else:
        # 如果没有传入, 获取最新一年assessment信息
        assessment_orm_list = Assessment.query.filter_by(course_code=course_code).all()
        year_list = []
        for ass_orm in assessment_orm_list:
            year_list.append(int(ass_orm.year, 10))
        year = max(year_list)
        assessment_orm_list = Assessment.query.filter_by(course_code=course_code, year=year).all()

    for assessment_orm in assessment_orm_list:
        course['assessment'].append({
            'method': assessment_orm.method,
            'weight': assessment_orm.percentage,
            'cilostr': assessment_orm.cilostr,
            'year': assessment_orm.year
        })


    # 获取前置CILO关系
    pre_course_code_list = [] # 获取前置课程 course code
    pre_relation_orm_list = Pre.query.filter_by(post_course=course_code).all()
    for pre_relation in pre_relation_orm_list:
        if pre_relation.pre_course not in pre_course_code_list:
            pre_course_code_list.append(pre_relation.pre_course)
        course['prerequisite_relation'].append({
            'current_cilo_index': pre_relation.post_cilo_index,
            'pre_course_code': pre_relation.pre_course,
            'pre_cilo_index': pre_relation.pre_cilo_index
        })

    # 获取前置课程详细信息
    for pre_course_code in pre_course_code_list:
        pre_course = Course.query.filter_by(course_code=pre_course_code).first()
        course['prerequisite_course'].append({
            'code': pre_course.course_code,
            'name': pre_course.course_name,
            'type': pre_course.course_type
        })

    # ----------------- 后置课程 ------------------------------------------------------------|
    # 获取用这门课作为前置课程的CILO信息
    post_course_code_list = [] # 获取后置课程的 course code
    post_relation_orm_list = Pre.query.filter_by(pre_course=course_code).all()
    for post_relation in post_relation_orm_list:
        if post_relation.post_course not in post_course_code_list:
            post_course_code_list.append(post_relation.post_course)
        course['post_relation'].append({
            'post_course_code': post_relation.post_course,
            'post_cilo_index': post_relation.post_cilo_index,
            'pre_cilo_index': post_relation.pre_cilo_index
        })

    # 获取用这门课作课程的为前置课程信息
    for post_course_code in post_course_code_list:
        post_course = Course.query.filter_by(course_code=post_course_code).first()
        course['post_courses'].append({
            'code': post_course.course_code,
            'name': post_course.course_name,
            'type': post_course.course_type
        })


    return jsonify({
        'code': 200,
        'info': 'get detail successfully',
        'result': course
    })


@course.route("/get_course_dependency_all", methods=['GET'])
@auth.login_required
def get_course_dependency():

    program = request.args.get('courseProgram')
    course_orm = Course.query.filter_by(department=program).all()
    course_code_list = []
    #Find all courses in this programme
    for course in course_orm:
        course_code_list.append(course.course_code)

    course = {
        'name': '',
        'code': '',
        'type': '',
        'CILO': [],
    }
    course_list = []
    course_relation_list = []
    cilo_relation_list = []
    cilo = {
        'cilo': '',
        'course': ''
    }
    CILO_list = [] # Contains cilos of all courses in this programme

    # 对应的课程
    for course_code in course_code_list:
        cilo_counter = 0
        course_orm = Course.query.filter_by(course_code=course_code).first()
        course['name'] = course_orm.course_name
        course['code'] = course_orm.course_code
        course['type'] = course_orm.course_type

        # 获取CILO
        current_course_cilo_list = CILO.query.filter_by(course_code=course_code).all()

        for current_course_cilo in current_course_cilo_list:
            course['CILO'].append(current_course_cilo.content)
            cilo = {
                'cilo': current_course_cilo.content,
                'course': course_code,
                'name': course_orm.course_name
            }
            CILO_list.append(cilo)
            cilo_counter = cilo_counter+1

        course_list.append(course)
        course = {
            'name': '',
            'code': '',
            'type': '',
            'CILO': [],
        }

        # 获取前置
        pre_course_list = Pre.query.filter_by(post_course=course_code).all()

        # 找到去重后的pre course code
        pre_course_code_list = []
        for pre_course in pre_course_list:
            if pre_course.pre_course not in pre_course_code_list:
                pre_course_code_list.append(pre_course.pre_course)


        for cilo in range(cilo_counter):
            cilo_index = cilo+1
            pre_course_list = Pre.query.filter_by(post_course=course_code, post_cilo_index=cilo_index).all()
            # 找到同一个课程同一个cilo下的所有type并去重
            type_list = []
            for relation in pre_course_list:
                if relation.type not in type_list:
                    type_list.append(relation.type)

            for type in type_list:
                cilo_content = CILO.query.filter_by(course_code=course_code,index=cilo_index).first()
                cilo_relation = {
                    'current_course':course_code,
                    'current_course_name': course_orm.course_name,
                    'current_cilo':cilo_content.content,
                    'pre_course': [],
                    'pre_course_name': [],
                    'pre_cilo': []
                }

                for relation in pre_course_list:
                    # type相同，cilos之间是or关系
                    if relation.type == type:
                        cilo_relation['pre_course'].append(relation.pre_course)
                        course_name = Course.query.filter_by(course_code=relation.pre_course).first()
                        cilo_relation['pre_course_name'].append(course_name.course_name)
                        cilo_content = CILO.query.filter_by(course_code=relation.pre_course, index=relation.pre_cilo_index).first()
                        cilo_relation['pre_cilo'].append(cilo_content.content)
                cilo_relation_list.append(cilo_relation)

    #根据cilo间的关系找到course间的关系
    for relation in cilo_relation_list:
        course_relation = {
            'current': relation['current_course'],
            'current_name': relation['current_course_name'],
            'pre': [],
            'pre_name': []
        }
        #给relation['pre_course']里的课去重
        pre_list = []
        pre_name_list = []
        for pre in relation['pre_course']:
            if pre not in pre_list:
                pre_list.append(pre)
        for pre_name in relation['pre_course_name']:
            if pre_name not in pre_name_list:
                pre_name_list.append(pre_name)
        course_relation['pre'].append(pre_list)
        course_relation['pre_name'].append(pre_name_list)
        if course_relation not in course_relation_list:
            course_relation_list.append(course_relation)

    return jsonify({
        'code': 200,
        'info': 'get course dependency successfully',
        'result': {
            'cilo': CILO_list,
            'cilo_relation': cilo_relation_list,
            'course_info': course_list,
            'course_relation': course_relation_list
        }
    })


@course.route('/get_all_program', methods=['GET'])
def get_all_program():
    program_list = []
    course_orm_list = Course.query.all()
    for course_orm in course_orm_list:
        if course_orm.department not in program_list:
            program_list.append(course_orm.department)
    return jsonify({
        'code': 200,
        'info': 'query program list successfully',
        'result': program_list
    })