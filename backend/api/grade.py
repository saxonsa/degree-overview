from flask import Blueprint, request, jsonify
from models.base import db
from models.grade import Grade
from models.taken import Taken
from models.cilo import CILO
from models.assessment import Assessment
from models.uni_cilo import Uni_CILO
from models.semes_cilo import Semes_CILO
from .token_auth import auth
import datetime

grade = Blueprint("grade", __name__)


@grade.route('/calculate_student_total_score_by_id_and_course', methods=['GET'])
@auth.login_required
def calculate_total_grade():
    '''
    description: calculate student total score on one course based on the grade of sub-section assessment
                (assessment: Labs, Projects, Assignment...)
    :param @stuid: Student ID
    :param @course_code: Course code
    Action: Calculate taken score field
    '''
    stuid = request.args.get('stuid')
    course_code = request.args.get('courseCode')

    partial_score = Grade.query.filter_by(stuid=stuid, course_code=course_code).all()

    total_score = 0
    for score in partial_score:
        total_score += score.partial_score

    # modify total_score in database
    # total_score_record = Taken.query.filter_by(studentID=stuid, course_code=course_code).first()
    # total_score_record.total_score = total_score
    # db.session.commit()

    return jsonify({
        'code': 200,
        'info': 'query total score on ' + course_code + ' success',
        'return': {
            'total_score': total_score
        }
    })


# calculate individual learning performance on various learning outcome
@grade.route('/calculate_personal_cilo_score', methods=['GET'])
def calculate_personal_cilo_score():
    '''
    Description: Calculate personal CILOs score on one course (All CILOs)
    :param stuid: Student ID
    :param course_code: Course code
    :return: query individual CILOs score
    '''

    stuid = request.args.get('stuid')
    course_code = request.args.get('courseCode')

    # 找到这门course的所有CILO, 并存到cilo_index_list列表中 [1, 2, 3]
    cilo_list = CILO.query.filter_by(course_code=course_code)
    cilo_index_list = []
    for cilo in cilo_list:
        cilo_index_list.append(cilo.index)



    score_list = []
    ass_cilo_list = Assessment.query.filter_by(course_code=course_code)
    for index in cilo_index_list:
        uni_cilo_dir = {'cilo_index': index, 'cilo_score': 0, 'cilo_total': 0, 'cilo_performance': 0.0}

        # calculate the distribution of full marks on each CILO
        for ass_cilo in ass_cilo_list:
            ass_sub_cilo_list1 = ass_cilo.cilostr.split("-")
            if str(index) in ass_sub_cilo_list1:
                percentage = Assessment.query.filter_by(course_code=course_code,
                                                        method=ass_cilo.method).first().percentage
                if len(ass_sub_cilo_list1) == 1:
                    uni_cilo_dir['cilo_total'] += percentage
                else:
                    uni_cilo_dir['cilo_total'] += percentage / len(ass_sub_cilo_list1)

        # calculate sub-cilo score
        for ass_cilo in ass_cilo_list:
            ass_sub_cilo_list2 = ass_cilo.cilostr.split("-")
            if str(index) in ass_sub_cilo_list2:
                partial_score = Grade.query.filter_by(stuid=stuid, course_code=course_code,
                                                      ass_method=ass_cilo.method).first().partial_score
                if len(ass_sub_cilo_list2) == 1:
                    uni_cilo_dir['cilo_score'] += partial_score
                else:
                    uni_cilo_dir['cilo_score'] += partial_score / len(ass_sub_cilo_list2)

        # calculate performance: performance = (cilo_score / cilo_total) %
        uni_cilo_dir['cilo_performance'] = round(uni_cilo_dir['cilo_score'] / uni_cilo_dir['cilo_total'], 2)

        # add performance to database
        # uni_cilo = Uni_CILO(studentID=stuid, course_code=course_code, cilo_index=uni_cilo_dir['cilo_index'],
        #                     cilo_performance=uni_cilo_dir['cilo_performance'])
        # db.session.add(uni_cilo)
        # db.session.commit()
        score_list.append(uni_cilo_dir)

    return jsonify({
        'code': 200,
        'info': 'calculate successfully',
        'result': {
            'cilo_score': score_list
        }
    })


def calculate_student_cilo_score(stuid, course_code):
    # 找到这门course的所有CILO, 并存到cilo_index_list列表中 [1, 2, 3]
    cilo_list = CILO.query.filter_by(course_code=course_code)
    cilo_index_list = []
    for cilo in cilo_list:
        cilo_index_list.append(cilo.index)

    score_list = []
    ass_cilo_list = Assessment.query.filter_by(course_code=course_code)
    for index in cilo_index_list:
        uni_cilo_dir = {'cilo_index': index, 'cilo_score': 0, 'cilo_total': 0, 'cilo_performance': 0.0}

        # calculate the distribution of full marks on each CILO
        for ass_cilo in ass_cilo_list:
            ass_sub_cilo_list1 = ass_cilo.cilostr.split("-")
            if str(index) in ass_sub_cilo_list1:
                percentage = Assessment.query.filter_by(course_code=course_code,
                                                        method=ass_cilo.method).first().percentage
                if len(ass_sub_cilo_list1) == 1:
                    uni_cilo_dir['cilo_total'] += percentage
                else:
                    uni_cilo_dir['cilo_total'] += percentage / len(ass_sub_cilo_list1)

        # calculate sub-cilo score
        for ass_cilo in ass_cilo_list:
            ass_sub_cilo_list2 = ass_cilo.cilostr.split("-")
            if str(index) in ass_sub_cilo_list2:
                partial_score = Grade.query.filter_by(stuid=stuid, course_code=course_code,
                                                      ass_method=ass_cilo.method).first().partial_score
                if len(ass_sub_cilo_list2) == 1:
                    uni_cilo_dir['cilo_score'] += partial_score
                else:
                    uni_cilo_dir['cilo_score'] += partial_score / len(ass_sub_cilo_list2)

        # calculate performance: performance = (cilo_score / cilo_total) %
        uni_cilo_dir['cilo_performance'] = round(uni_cilo_dir['cilo_score'] / uni_cilo_dir['cilo_total'], 2)

        # add performance to database
        # uni_cilo = Uni_CILO(studentID=stuid, course_code=course_code, cilo_index=uni_cilo_dir['cilo_index'],
        #                     cilo_performance=uni_cilo_dir['cilo_performance'])
        # db.session.add(uni_cilo)
        # db.session.commit()
        score_list.append(uni_cilo_dir)

    return score_list


@grade.route('/calculate_average_year_cilo_score_for_result_analysis', methods=['GET'])
def calculate_average_year_cilo_score_for_result_analysis():

    course_code = request.args.get('course_code')

    # 找到这门course的所有CILO, 并存到cilo_index_list列表中 [1, 2, 3]
    cilo_list = CILO.query.filter_by(course_code=course_code)
    cilo_index_list = []
    for cilo in cilo_list:
        cilo_index_list.append(cilo.index)

    ass_cilo_list = Assessment.query.filter_by(course_code=course_code)

    # 近10年成绩
    year_score_list = []
    current_year = datetime.datetime.now().year
    for year in range(current_year - 9, current_year + 1):

        # 找到在这一年上这门课的学生的学号
        year_str = str(year)
        stuid_list = []
        taken_orm_list = Taken.query.filter_by(year=year_str, course_code=course_code).all()
        num_of_student = Taken.query.filter_by(year=year_str, course_code=course_code).count() # 上这门课学生的总人数
        if num_of_student == 0:
            # 如果没有学生就进入下一年的计算
            continue

        for taken_orm in taken_orm_list:
            stuid_list.append(taken_orm.stuid)

        # 计算所有学生的所有CILO成绩
        cilo_score = {}
        for cilo_index in cilo_index_list:
            cilo_score['index' + str(cilo_index)] = 0

        for stuid in stuid_list:
            score_list = calculate_student_cilo_score(stuid, course_code)
            index = -1
            for cilo_index in cilo_index_list:
                index += 1
                cilo_score['index' + str(cilo_index)] += score_list[index]['cilo_performance']

        # 将所得的CILO取平均
        for cilo_index in cilo_index_list:
            cilo_score['index' + str(cilo_index)] /= num_of_student

        year_score_list.append({
            'year': year_str,
            'cilo_score': cilo_score
        })

    return jsonify({
        'code': 200,
        'info': 'calculate average cilo score successfully',
        'result': year_score_list
    })


# calculate all students learning performance on various learning outcome on semester basis
@grade.route('/calculate_semes_cilo_score', methods=['POST'])
def calculate_semes_cilo_score():
    course_code = request.args.get('course_code')
    year = request.args.get('year')
    semester = request.args.get('semester')

    semes_cilo_record = {'cilo_index': 0, 'semes_cilo_score': 0.0}

    # get student ID List for them who take this course
    stuid_list = []
    taken_records_list = Taken.query.filter_by(course_code=course_code, year=year, semester=semester)
    for taken_record in taken_records_list:
        stuid_list.append(taken_record.studentID)

    # get cilo index list of this course
    cilo_index_list = []
    cilo_records_list = CILO.query.filter_by(course_code=course_code)
    for cilo_record in cilo_records_list:
        cilo_index_list.append(cilo_record.index)

    for cilo_index in cilo_index_list:
        semes_cilo_record['semes_cilo_score'] = 0
        semes_cilo_record['cilo_index'] = cilo_index

        for stuid in stuid_list:
            unicilo_record = Uni_CILO.query.filter_by(studentID=stuid, course_code=course_code,
                                                      cilo_index=cilo_index).first()
            semes_cilo_record['semes_cilo_score'] += unicilo_record.cilo_performance

        semes_cilo_record['semes_cilo_score'] = round(semes_cilo_record['semes_cilo_score'] / len(stuid_list), 2)

        # add semester cilo score into database
        semes_cilo = Semes_CILO(course_code=course_code, year=year, semester=semester, cilo_index=cilo_index,
                                semes_cilo_score=semes_cilo_record['semes_cilo_score'])
        db.session.add(semes_cilo)
        db.session.commit()


    return jsonify({
        'info': 'calculate semester cilo score successfully',
        'return': 1
    })


# calculate CILO average score
@grade.route('/calculate_cilo_avg_score', methods=['POST'])
def calculate_cilo_avg_score():
    course_code = request.args.get('course_code')

    # get cilo index list of this course
    cilo_index_list = []
    cilo_records_list = CILO.query.filter_by(course_code=course_code)
    for cilo_record in cilo_records_list:
        cilo_index_list.append(cilo_record.index)

    cilo_avg_record = {'cilo_index': 0, 'avg_score': 0.0}
    numOfSemesCILO = 0
    for cilo_index in cilo_index_list:
        cilo_avg_record['cilo_index'] = cilo_index
        cilo_avg_record['avg_score'] = 0.0
        numOfSemesCILO = 0

        semes_cilo_records_list = Semes_CILO.query.filter_by(course_code=course_code, cilo_index=cilo_index)
        for semes_cilo_record in semes_cilo_records_list:
            numOfSemesCILO += 1
            cilo_avg_record['avg_score'] += semes_cilo_record.semes_cilo_score
        cilo_avg_record['avg_score'] = round(cilo_avg_record['avg_score'] / numOfSemesCILO, 2)

        cilos_record = CILO.query.filter_by(course_code=course_code, index=cilo_index).first()
        cilos_record.avg_score = cilo_avg_record['avg_score']
        # db.session.commit()

    return jsonify({
        'info': 'calculate_cilo_avg_score successfully',
        'return': 1
    })