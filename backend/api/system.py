from flask import Blueprint, request, jsonify
from models.course import Course
from models.cilo import CILO
from models.pre import Pre
from models.taken import Taken
from math import ceil
from .token_auth import auth


system = Blueprint("system", __name__)


@system.route("/search_course", methods=['GET'])
def search_course():
    """
    通过type和keyword来检索课程
    :return:
    """
    # 请求的页码, 默认为 1
    page = request.args.get('page', 1, type=int)

    # 请求的参数
    keyword = request.args.get('keyword')
    type = request.args.get('type')

    # page参数
    per_page = 9
    total_page_num = 1

    course_list = []

    if type == 'by name':
        total_page_num = ceil(Course.query.filter(
            Course.course_name.like("%" + keyword + "%") if keyword is not None else ""
        ).count() / per_page)

        pagination = Course.query.filter(
            Course.course_name.like("%" + keyword + "%") if keyword is not None else ""
        ).order_by(Course.course_code.asc()).paginate(
            page, per_page=per_page,
            error_out=False
        )
        course_orm_list = pagination.items

        # course_orm_list = Course.query.filter(
        #     Course.course_name.like("%" + keyword + "%") if keyword is not None else ""
        # ).all()
        course_list = []
        for course_orm in course_orm_list:
            course = {
                'course_code': course_orm.course_code,
                'course_type': course_orm.course_type,
                'course_name': course_orm.course_name,
                'course_unit': course_orm.unit,
                'course_department': course_orm.department
            }
            course_list.append(course)

    elif type == 'by code':
        total_page_num = ceil(Course.query.filter(
            Course.course_code.like("%" + keyword + "%") if keyword is not None else ""
        ).count() / per_page)

        pagination = Course.query.filter(
            Course.course_code.like("%" + keyword + "%") if keyword is not None else ""
        ).order_by(Course.course_code.asc()).paginate(
            page, per_page=per_page,
            error_out=False
        )
        course_orm_list = pagination.items

        # course_orm_list = Course.query.filter(
        #     Course.course_code.like("%" + keyword + "%") if keyword is not None else ""
        # ).all()

        course_list = []
        for course_orm in course_orm_list:
            course = {
                'course_code': course_orm.course_code,
                'course_type': course_orm.course_type,
                'course_name': course_orm.course_name,
                'course_unit': course_orm.unit,
                'course_department': course_orm.department
            }
            course_list.append(course)

    elif type == 'by unit':
        total_page_num = ceil(Course.query.filter(unit=keyword).count() / per_page)

        pagination = Course.query.filter(unit=keyword).order_by(Course.course_code.asc()).paginate(
            page, per_page=per_page,
            error_out=False
        )
        course_orm_list = pagination.items

        # course_orm_list = Course.query.filter_by(unit=keyword).all()
        course_list = []
        for course_orm in course_orm_list:
            course = {
                'course_code': course_orm.course_code,
                'course_type': course_orm.course_type,
                'course_name': course_orm.course_name,
                'course_unit': course_orm.unit,
                'course_department': course_orm.department
            }
            course_list.append(course)

    elif type == 'by type':
        total_page_num = ceil(Course.query.filter(
            Course.course_type.like("%" + keyword + "%") if keyword is not None else ""
        ).count() / per_page)

        pagination = Course.query.filter(
            Course.course_type.like("%" + keyword + "%") if keyword is not None else ""
        ).order_by(Course.course_code.asc()).paginate(
            page, per_page=per_page,
            error_out=False
        )
        course_orm_list = pagination.items

        # course_orm_list = Course.query.filter(
        #     Course.course_type.like("%" + keyword + "%") if keyword is not None else ""
        # ).all()
        course_list = []
        for course_orm in course_orm_list:
            course = {
                'course_code': course_orm.course_code,
                'course_type': course_orm.course_type,
                'course_name': course_orm.course_name,
                'course_unit': course_orm.unit,
                'course_department': course_orm.department
            }
            course_list.append(course)


    elif type == 'by course (with code)':


        # !!! NB: 假设一个课程没有超过8个前置课程, 因为此处没有做分页处理

        total_page_num = 1

        # 看看符合搜索条件的有多少门课程
        current_course_num = Course.query.filter(
            Course.course_code.like("%" + keyword + "%") if keyword is not None else ""
        ).count()


        # 如果查询到多门符合的课程, 返回错误信息
        if current_course_num > 1:
            return jsonify({
                'code': "5000",
                'info': 'Sorry, We found' + str(current_course_num) + 'qualified courses, please add more details!'
            })

        else:
            # 如果只有一个符合的, 找到这门课 (只返回第一个符合的)
            current_course = Course.query.filter_by(course_code=keyword).first()

            course_list = []
            course = {
                'course_code': current_course.course_code,
                'course_name': current_course.course_name,
                'course_type': current_course.course_type,
                'cilo': [],
                'prerequisite_course': []
            }

            # 找到课程的CILO
            cilos = CILO.query.filter_by(course_code=keyword).all()
            for cilo in cilos:
                course['cilo'].append({
                    'cilo_index': cilo.index,
                    'cilo_content': cilo.content
                })

            # 获取前置课程代号
            pre_course_list = []
            prerequisites_num = Pre.query.filter_by(post_course=current_course.course_code).count()
            prerequisites = Pre.query.filter_by(post_course=current_course.course_code).all()
            for pre_relation in prerequisites:
                if pre_relation.pre_course not in pre_course_list:
                    pre_course_list.append(pre_relation.pre_course)

            # 获取前置课程信息
            for pre_course_code in pre_course_list:
                pre_course = Course.query.filter_by(course_code=pre_course_code).order_by(
                    Course.course_name.asc()).first()
                prerequisite_course = {}
                prerequisite_course['course_type'] = pre_course.course_type
                prerequisite_course['course_code'] = pre_course.course_code
                prerequisite_course['course_name'] = pre_course.course_name
                prerequisite_course['cilo'] = []
                prerequisite_course['prerequisite_course'] = []

                # 获取前置课程的CILO
                cilos = CILO.query.filter_by(course_code=pre_course_code).all()
                for cilo in cilos:
                    prerequisite_course['cilo'].append({
                        'cilo_index': cilo.index,
                        'cilo_content': cilo.content
                    })

                course['prerequisite_course'].append(prerequisite_course)

            course_list.append(course)

    elif type == 'by keyword':

        # 查询keyword
        cilo_result_list = []

        # 对应的课程
        cilo_orm_list = CILO.query.filter(
            CILO.content.like("%" + keyword + "%") if keyword is not None else ""
        ).all()

        for cilo_orm in cilo_orm_list:
            result = {
                'current': {
                    'cilo_index': '',
                    'cilo_content': '',
                    'course': {
                        'name': '',
                        'code': '',
                        'type': ''
                    }
                },
                'pre': [],
                'post': []
            }

            # 现在查询到的CILO
            result['current']['cilo_index'] = cilo_orm.index
            result['current']['cilo_content'] = cilo_orm.content

            course_code = cilo_orm.course_code

            course_orm = Course.query.filter_by(course_code=course_code).first()
            result['current']['course']['name'] = course_orm.course_name
            result['current']['course']['code'] = course_orm.course_code
            result['current']['course']['type'] = course_orm.course_type

            # 前置CILO
            pre_orm_list = Pre.query.filter_by(post_course=course_code, post_cilo_index=cilo_orm.index)

            for pre_orm in pre_orm_list:
                pre_cilo_orm = CILO.query.filter_by(course_code=pre_orm.pre_course,
                                                    index=pre_orm.pre_cilo_index).first()
                pre = {
                    'cilo_index': pre_orm.pre_cilo_index,
                    'cilo_content': pre_cilo_orm.content,
                    'course': {
                        'name': '',
                        'code': '',
                        'type': ''
                    }
                }
                pre_course_orm = Course.query.filter_by(course_code=pre_orm.pre_course).first()
                pre['course']['name'] = pre_course_orm.course_name
                pre['course']['code'] = pre_course_orm.course_code
                pre['course']['type'] = pre_course_orm.course_type

                result['pre'].append(pre)

            # 后置CILO
            post_orm_list = Pre.query.filter_by(pre_course=course_code, pre_cilo_index=cilo_orm.index)

            for post_orm in post_orm_list:
                post_cilo_orm = CILO.query.filter_by(course_code=post_orm.post_course,
                                                     index=post_orm.post_cilo_index).first()
                post = {
                    'cilo_index': post_orm.post_cilo_index,
                    'cilo_content': post_cilo_orm.content,
                    'course': {
                        'name': '',
                        'code': '',
                        'type': ''
                    }
                }
                post_course_orm = Course.query.filter_by(course_code=post_orm.post_course).first()
                post['course']['name'] = post_course_orm.course_name
                post['course']['code'] = post_course_orm.course_code
                post['course']['type'] = post_course_orm.course_type

                result['post'].append(post)
            cilo_result_list.append(result)


        # 查询course
        current_course_list = []


        pre_course_list = []
        pre_course_code_list = []
        post_course_list = []
        post_course_code_list = []

        # 对应的课程
        name_orm_list = Course.query.filter(
            Course.course_name.like("%" + keyword + "%") if keyword is not None else ""
        ).all()

        code_orm_list = Course.query.filter(
            Course.course_code.like("%" + keyword + "%") if keyword is not None else ""
        ).all()

        # cilo_orm_list = CILO.query.filter(
        #     CILO.content.like("%" + keyword + "%") if keyword is not None else ""
        # ).all()

        current_course_code_list = []  # 对应现在CILO的课程code列表
        # for cilo_orm in cilo_orm_list:
        #     if cilo_orm.course_code not in current_course_code_list:
        #         current_course_code_list.append(cilo_orm.course_code)
        for name_orm in name_orm_list:
            if name_orm.course_code not in current_course_code_list:
                current_course_code_list.append(name_orm.course_code)
        for code_orm in code_orm_list:
            if code_orm.course_code not in current_course_code_list:
                current_course_code_list.append(code_orm.course_code)

        for current_course_code in current_course_code_list:
            course = {
                'course_name': '',
                'course_code': '',
                'course_type': '',
                'cilo': [],
                'prerequisite_course': []
            }
            course_orm = Course.query.filter_by(course_code=current_course_code).first()
            course['course_name'] = course_orm.course_name
            course['course_code'] = course_orm.course_code
            course['course_type'] = course_orm.course_type

            # 获取CILO
            current_course_cilo_list = CILO.query.filter_by(course_code=current_course_code).all()

            for current_course_cilo in current_course_cilo_list:
                course['cilo'].append(current_course_cilo.content)

            # 获取前置
            pre_course_orm_list = Pre.query.filter_by(post_course=current_course_code).all()
            for pre_course_orm in pre_course_orm_list:
                if pre_course_orm.pre_course not in pre_course_code_list:
                    pre_course_code_list.append(pre_course_orm.pre_course)

            for pre_course_code in pre_course_code_list:
                pre_course = Course.query.filter_by(course_code=pre_course_code).first()
                course['prerequisite_course'].append({
                    'course_code': pre_course.course_code,
                    'course_name': pre_course.course_name,
                    'course_type': pre_course.course_type
                })
            current_course_list.append(course)

        return jsonify({
            'code': '200',
            'info': 'search by keyword successfully',
            'search_type': 'by keyword',
            'result': {
                'cilo': cilo_result_list,
                'course': current_course_list
            },
        })

    elif type == 'by Course':

        current_course_code_list = []
        result_list = []

        # 找到对应的课程
        course_list_by_name = Course.query.filter(
            Course.course_name.like("%" + keyword + "%") if keyword is not None else "").all()
        course_list_by_code = Course.query.filter(
            Course.course_code.like("%" + keyword + "%") if keyword is not None else "").all()

        # 把两个list的所有课程放到一起
        for course in course_list_by_name:
            current_course_code_list.append(course.course_code)
        for course in course_list_by_code:
            if course not in current_course_code_list:
                current_course_code_list.append(course.course_code)
        
        # 对每个搜到的课程都有一组(pre,current,post),所有内容都写在这个循环里边
        for current_course_code in current_course_code_list:
            # 对于每个current course都清空这些信息
            pre_course_code_list = []
            post_course_code_list = []

            course = {
                'name': '',
                'code': '',
                'type': '',
                'CILO': [],
            }

            result = {
                'pre': [],
                'current': course,
                'post': [],
            }


            # 找到这门课程自身的信息
            course_orm = Course.query.filter_by(course_code = current_course_code).first()
            course['name'] = course_orm.course_name
            course['code'] = course_orm.course_code
            course['type'] = course_orm.course_type
            # 获取current course的CILO
            current_course_cilo_list = CILO.query.filter_by(course_code=current_course_code).all()
            for current_course_cilo in current_course_cilo_list:
                course['CILO'].append(current_course_cilo.content)
            result['current'] = course

            # 找到该门课的所有前置课程的course_code
            pre_course_list = Pre.query.filter_by(post_course=current_course_code).all()
            for pre_course in pre_course_list:
                if pre_course.pre_course not in pre_course_code_list:
                    pre_course_code_list.append(pre_course.pre_course)
            print(pre_course_code_list)
            for pre_course_code in pre_course_code_list:
                pre_course_obj = {
                    'name': '',
                    'code': '',
                    'type': '',
                    'CILO': [],
                }
                pre_course = Course.query.filter_by(course_code=pre_course_code).first()
                pre_course_obj['name'] = pre_course.course_name
                pre_course_obj['code'] = pre_course.course_code
                pre_course_obj['type'] = pre_course.course_type

                # 获取CILO
                pre_course_cilo_list = CILO.query.filter_by(course_code=pre_course_code).all()

                for pre_course_cilo in pre_course_cilo_list:
                    pre_course_obj['CILO'].append(pre_course_cilo.content)

                result['pre'].append(pre_course_obj)

            # 找到这门课程所有的后置课程
            post_course_list = Pre.query.filter_by(pre_course = current_course_code).all()
            for post_course in post_course_list:
                if post_course.post_course not in post_course_code_list:
                    post_course_code_list.append(post_course.post_course)

            for post_course_code in post_course_code_list:
                post_course_obj = {
                    'name': '',
                    'code': '',
                    'type': '',
                    'CILO': [],
                }
                post_course = Course.query.filter_by(course_code=post_course_code).first()
                post_course_obj['name'] = post_course.course_name
                post_course_obj['code'] = post_course.course_code
                post_course_obj['type'] = post_course.course_type

                # 获取CILO
                post_course_cilo_list = CILO.query.filter_by(course_code=post_course_code).all()

                for post_course_cilo in post_course_cilo_list:
                    post_course_obj['CILO'].append(post_course_cilo.content)

                result['post'].append(post_course_obj)


            # 现在的result里包含了current course的前置课程名字，自身信息，后置课程名字
            result_list.append(result)
        print(result_list)

        return jsonify({
            'code': '200',
            'info': 'search by course successfully',
            'total_page': 1,
            'search_type': 'by Course',
            'result': result_list
        })


    elif type == 'by CILO':

        index_list = []
        result_list = []

        # 对应的课程
        cilo_orm_list = CILO.query.filter(
            CILO.content.like("%" + keyword + "%") if keyword is not None else ""
        ).all()

        for cilo_orm in cilo_orm_list:
            result = {
                'current': {
                    'cilo_index': '',
                    'cilo_content': '',
                    'course': {
                        'name': '',
                        'code': '',
                        'type': ''
                    }
                },
                'pre': [],
                'post': []
            }

            # 现在查询到的CILO
            result['current']['cilo_index'] = cilo_orm.index
            result['current']['cilo_content'] = cilo_orm.content

            course_code = cilo_orm.course_code

            course_orm = Course.query.filter_by(course_code=course_code).first()
            result['current']['course']['name'] = course_orm.course_name
            result['current']['course']['code'] = course_orm.course_code
            result['current']['course']['type'] = course_orm.course_type

            # 前置CILO
            pre_orm_list = Pre.query.filter_by(post_course=course_code, post_cilo_index=cilo_orm.index)

            for pre_orm in pre_orm_list:
                pre_cilo_orm = CILO.query.filter_by(course_code=pre_orm.pre_course, index=pre_orm.pre_cilo_index).first()
                pre = {
                    'cilo_index': pre_orm.pre_cilo_index,
                    'cilo_content': pre_cilo_orm.content,
                    'course': {
                        'name': '',
                        'code': '',
                        'type': ''
                    }
                }
                pre_course_orm = Course.query.filter_by(course_code=pre_orm.pre_course).first()
                pre['course']['name'] = pre_course_orm.course_name
                pre['course']['code'] = pre_course_orm.course_code
                pre['course']['type'] = pre_course_orm.course_type

                result['pre'].append(pre)

            # 后置CILO
            post_orm_list = Pre.query.filter_by(pre_course=course_code, pre_cilo_index=cilo_orm.index)

            for post_orm in post_orm_list:
                post_cilo_orm = CILO.query.filter_by(course_code=post_orm.post_course, index=post_orm.post_cilo_index).first()
                post = {
                    'cilo_index': post_orm.post_cilo_index,
                    'cilo_content': post_cilo_orm.content,
                    'course': {
                        'name': '',
                        'code': '',
                        'type': ''
                    }
                }
                post_course_orm = Course.query.filter_by(course_code=post_orm.post_course).first()
                post['course']['name'] = post_course_orm.course_name
                post['course']['code'] = post_course_orm.course_code
                post['course']['type'] = post_course_orm.course_type

                result['post'].append(post)
            result_list.append(result)



        # current_course_code_list = []  # 对应现在CILO的课程code列表
        # for cilo_orm in cilo_orm_list:
        #
        #     if cilo_orm.course_code not in current_course_code_list:
        #         current_course_code_list.append(cilo_orm.course_code)
        #
        # # 对每个搜到的课程都有一组(pre,current,post),所有内容都写在这个循环里边
        # for current_course_code in current_course_code_list:
        #     # 对于每个current course都清空这些信息
        #     pre_course_code_list = []
        #     post_course_code_list = []
        #
        #     course = {
        #         'name': '',
        #         'code': '',
        #         'type': '',
        #         'CILO': [],
        #     }
        #
        #     result = {
        #         'pre': [],
        #         'current': course,
        #         'post': [],
        #     }
        #
        #     # 找到这门课程自身的信息
        #     course_orm = Course.query.filter_by(course_code=current_course_code).first()
        #     course['name'] = course_orm.course_name
        #     course['code'] = course_orm.course_code
        #     course['type'] = course_orm.course_type
        #     # 获取current course的CILO
        #     current_course_cilo_list = CILO.query.filter_by(course_code=current_course_code).all()
        #     for current_course_cilo in current_course_cilo_list:
        #         course['CILO'].append(current_course_cilo.content)
        #
        #     result['current'] = course
        #
        #     # 找到该门课的所有前置课程的course_code
        #     pre_course_list = Pre.query.filter_by(post_course=current_course_code).all()
        #     for pre_course in pre_course_list:
        #         if pre_course.pre_course not in pre_course_code_list:
        #             pre_course_code_list.append(pre_course.pre_course)
        #
        #     for pre_course_code in pre_course_code_list:
        #         pre_course_obj = {
        #             'name': '',
        #             'code': '',
        #             'type': '',
        #             'CILO': [],
        #         }
        #         pre_course = Course.query.filter_by(course_code=pre_course_code).first()
        #         pre_course_obj['name'] = pre_course.course_name
        #         pre_course_obj['code'] = pre_course.course_code
        #         pre_course_obj['type'] = pre_course.course_type
        #
        #         # 获取CILO
        #         pre_course_cilo_list = CILO.query.filter_by(course_code=pre_course_code).all()
        #
        #         for pre_course_cilo in pre_course_cilo_list:
        #             pre_course_obj['CILO'].append(pre_course_cilo.content)
        #
        #         result['pre'].append(pre_course_obj)
        #
        #     # 找到这门课程所有的后置课程
        #     post_course_list = Pre.query.filter_by(pre_course=current_course_code).all()
        #     for post_course in post_course_list:
        #         if post_course.post_course not in post_course_code_list:
        #             post_course_code_list.append(post_course.post_course)
        #
        #     for post_course_code in post_course_code_list:
        #         post_course_obj = {
        #             'name': '',
        #             'code': '',
        #             'type': '',
        #             'CILO': [],
        #         }
        #         post_course = Course.query.filter_by(course_code=post_course_code).first()
        #         post_course_obj['name'] = post_course.course_name
        #         post_course_obj['code'] = post_course.course_code
        #         post_course_obj['type'] = post_course.course_type
        #
        #         # 获取CILO
        #         post_course_cilo_list = CILO.query.filter_by(course_code=post_course_code).all()
        #
        #         for post_course_cilo in post_course_cilo_list:
        #             post_course_obj['CILO'].append(post_course_cilo.content)
        #
        #         result['post'].append(post_course_obj)
        #
        #     # 现在的result里包含了current course的前置课程名字，自身信息，后置课程名字
        #     result_list.append(result)
        print(result_list)

        return jsonify({
            'code': '200',
            'info': 'search by cilo successfully',
            'total_page': 1,
            'search_type': 'by CILO',
            'result': result_list
        })

    else:
        pass

    response = {
        'code': "200",
        'info': 'success',
        'result': {
            'total_page': total_page_num,
            'course': course_list,
            'search_type': type
        }
    }
    return jsonify(response)

@system.route("/search_course_all", methods=['GET'])
@auth.login_required
def search_course_all():
    """
    展示所有课程
    :return:
        course: 所有课程的列表 (包括CILO和prerequisite课程等信息)
        total_page: 总页码
    """

    # 获取请求的页码, 默认为 1
    page = request.args.get('page', 1, type=int)

    # 每页展示9个
    per_page = 9

    # 获取请求页码的 course list
    pagination = Course.query.order_by(Course.course_code.asc()).paginate(
        page, per_page=per_page,
        error_out=False
    )
    course_orm_list = pagination.items

    # 获取总页码数量
    total_page_num = ceil(Course.query.count() / per_page)

    # 将内容需要的字段按格式写入 course_list 中
    course_list = []
    for course_orm in course_orm_list:
        course = {
            'course_code': course_orm.course_code,
            'course_type': course_orm.course_type,
            'course_name': course_orm.course_name,
            'course_unit': course_orm.unit,
            'course_department': course_orm.department,
            'cilo': [],
            'prerequisite_course': []
        }

        # 找到课程对应的 CILO, 并添加到对应课程的CILO对象中
        cilos = CILO.query.filter_by(course_code=course_orm.course_code).all()
        for cilo in cilos:
            course['cilo'].append({
                'cilo_index': cilo.index,
                'cilo_content': cilo.content
            })
        course_list.append(course)

        # ----------------------------------------------
        # 找到课程的前置课程, 并在prerequisite_course对象列表中返回
        # ----------------------------------------------
        # 找到前置课程code的列表
        pre_course_list = []
        prerequisites = Pre.query.filter_by(post_course=course_orm.course_code).all()
        for pre_relation in prerequisites:
            if pre_relation.pre_course not in pre_course_list:
                pre_course_list.append(pre_relation.pre_course)

        # 找到code对应的课程信息
        for pre_course_code in pre_course_list:
            pre_course = Course.query.filter_by(course_code=pre_course_code).order_by(Course.course_name.asc()).first()
            prerequisite_course = {}
            prerequisite_course['course_type'] = pre_course.course_type
            prerequisite_course['course_code'] = pre_course.course_code
            prerequisite_course['course_name'] = pre_course.course_name
            course['prerequisite_course'].append(prerequisite_course)


    # 返回请求结果
    response = {
        'code': "200",
        'info': 'success',
        'result': {
            'total_page': total_page_num,
            'course': course_list,
            'search_type': 'all'
        }
    }
    return jsonify(response)

@system.route("/search_course_by_keyword_in_dependency", methods=['GET'])
def search_course_by_keyword_in_dependency():

    type = request.args.get('searchType')
    keyword = request.args.get('searchKeyword')

    if type == 'Course':

        # 初始化要返回的course列表
        course_list = []

        course_code_list = []

        # ---------------- 获取 course 信息 ------------------------------------------------- ##
        # 通过 course code 来模糊查询到的 course 信息
        course_search_by_code_orm_list = Course.query.filter(
            Course.course_code.like("%" + keyword + "%") if keyword is not None else ""
        )
        # 通过course name 来模糊查询到的 course 信息
        course_search_by_name_orm_list = Course.query.filter(
            Course.course_name.like("%" + keyword + "%") if keyword is not None else ""
        )
        # 将通过上面两种方式获得的course信息整合为一个list
        # course_orm_list = course_search_by_code_orm_list.extend(course_search_by_name_orm_list)
        # ---------------------------------------------------------------------------------- ##

        for course_orm in course_search_by_code_orm_list:

            course = {
                'course_code': course_orm.course_code,
                'course_type': course_orm.course_type,
                'course_name': course_orm.course_name,
                'course_unit': course_orm.unit,
                'course_department': course_orm.department,
                'cilo': [],
                'prerequisite_course': []
            }

            # 找到课程对应的 CILO, 并添加到对应课程的CILO对象中
            cilos = CILO.query.filter_by(course_code=course_orm.course_code).all()
            for cilo in cilos:
                course['cilo'].append({
                    'cilo_index': cilo.index,
                    'cilo_content': cilo.content
                })
            course_list.append(course)
            course_code_list.append(course_orm.course_code)

            # ----------------------------------------------
            # 找到课程的前置课程, 并在prerequisite_course对象列表中返回
            # ----------------------------------------------
            # 找到前置课程code的列表
            pre_course_list = []
            prerequisites = Pre.query.filter_by(post_course=course_orm.course_code).all()
            for pre_relation in prerequisites:
                if pre_relation.pre_course not in pre_course_list:
                    pre_course_list.append(pre_relation.pre_course)
            # 找到code对应的课程信息
            for pre_course_code in pre_course_list:
                pre_course = Course.query.filter_by(course_code=pre_course_code).order_by(
                    Course.course_name.asc()).first()
                prerequisite_course = {}
                prerequisite_course['course_type'] = pre_course.course_type
                prerequisite_course['course_code'] = pre_course.course_code
                prerequisite_course['course_name'] = pre_course.course_name
                course['prerequisite_course'].append(prerequisite_course)

        for course_orm in course_search_by_name_orm_list:

            # 排除掉已经用code搜到的课程
            if course_orm.course_code in course_code_list:
                continue

            course = {
                'course_code': course_orm.course_code,
                'course_type': course_orm.course_type,
                'course_name': course_orm.course_name,
                'course_unit': course_orm.unit,
                'course_department': course_orm.department,
                'cilo': [],
                'prerequisite_course': []
            }

            # 找到课程对应的 CILO, 并添加到对应课程的CILO对象中
            cilos = CILO.query.filter_by(course_code=course_orm.course_code).all()
            for cilo in cilos:
                course['cilo'].append({
                    'cilo_index': cilo.index,
                    'cilo_content': cilo.content
                })
            course_list.append(course)

            # ----------------------------------------------
            # 找到课程的前置课程, 并在prerequisite_course对象列表中返回
            # ----------------------------------------------
            # 找到前置课程code的列表
            pre_course_list = []
            prerequisites = Pre.query.filter_by(post_course=course_orm.course_code).all()
            for pre_relation in prerequisites:
                if pre_relation.pre_course not in pre_course_list:
                    pre_course_list.append(pre_relation.pre_course)
            # 找到code对应的课程信息
            for pre_course_code in pre_course_list:
                pre_course = Course.query.filter_by(course_code=pre_course_code).order_by(
                    Course.course_name.asc()).first()
                prerequisite_course = {}
                prerequisite_course['course_type'] = pre_course.course_type
                prerequisite_course['course_code'] = pre_course.course_code
                prerequisite_course['course_name'] = pre_course.course_name
                course['prerequisite_course'].append(prerequisite_course)

        # 返回请求结果
        response = {
            'code': "200",
            'info': 'success',
            'result': {
                'course': course_list,
                'search_type': 'course'
            }
        }
        return jsonify(response)

    else: # CILO

        # 初始化要返回的course列表
        course_list = []
        course_code_list = []

        CILO_orm_list = CILO.query.filter(
            CILO.content.like("%" + keyword + "%") if keyword is not None else ""
        )

        for CILO_orm in CILO_orm_list:
            course_code_list.append(CILO_orm.course_code)

        for course_code in course_code_list:
            course_orm = Course.query.filter_by(course_code=course_code).first()

            course = {
                'course_code': course_orm.course_code,
                'course_type': course_orm.course_type,
                'course_name': course_orm.course_name,
                'course_unit': course_orm.unit,
                'course_department': course_orm.department,
                'cilo': [],
                'prerequisite_course': []
            }

            # 找到课程对应的 CILO, 并添加到对应课程的CILO对象中
            # 注意: 此处只要 CILO content中包含Keyword的对应CILO
            # cilos = CILO.query.filter_by(course_code=course_orm.course_code, ).all()
            cilos = CILO.query.filter(
                CILO.course_code == course_orm.course_code,
                CILO.content.like("%" + keyword + "%") if keyword is not None else ""
            ).all()

            for cilo in cilos:
                course['cilo'].append({
                    'cilo_index': cilo.index,
                    'cilo_content': cilo.content
                })
            course_list.append(course)

            # ----------------------------------------------
            # 找到课程的前置课程, 并在prerequisite_course对象列表中返回
            # ----------------------------------------------
            # 找到前置课程code的列表
            pre_course_list = []
            prerequisites = Pre.query.filter_by(post_course=course_orm.course_code).all()
            for pre_relation in prerequisites:
                if pre_relation.pre_course not in pre_course_list:
                    pre_course_list.append(pre_relation.pre_course)
            # 找到code对应的课程信息
            for pre_course_code in pre_course_list:
                pre_course = Course.query.filter_by(course_code=pre_course_code).order_by(
                    Course.course_name.asc()).first()
                prerequisite_course = {}
                prerequisite_course['course_type'] = pre_course.course_type
                prerequisite_course['course_code'] = pre_course.course_code
                prerequisite_course['course_name'] = pre_course.course_name
                course['prerequisite_course'].append(prerequisite_course)

        # 返回请求结果
        response = {
            'code': "200",
            'info': 'success',
            'result': {
                'course': course_list,
                'search_type': 'CILO'
            }
        }
        return jsonify(response)


@system.route("/search_course_all_in_denpendency", methods=['GET'])
def search_course_all_in_dependency():

    course_list = []
    course_orm_list = Course.query.all()

    for course_orm in course_orm_list:
        course = {
            'course_code': course_orm.course_code,
            'course_type': course_orm.course_type,
            'course_name': course_orm.course_name,
            'course_unit': course_orm.unit,
            'course_department': course_orm.department,
            'cilo': [],
            'prerequisite_course': []
        }

        # 找到课程对应的 CILO, 并添加到对应课程的CILO对象中
        cilos = CILO.query.filter_by(course_code=course_orm.course_code).all()
        for cilo in cilos:
            course['cilo'].append({
                'cilo_index': cilo.index,
                'cilo_content': cilo.content
            })
        course_list.append(course)

        # ----------------------------------------------
        # 找到课程的前置课程, 并在prerequisite_course对象列表中返回
        # ----------------------------------------------
        # 找到前置课程code的列表
        pre_course_list = []
        prerequisites = Pre.query.filter_by(post_course=course_orm.course_code).all()
        for pre_relation in prerequisites:
            if pre_relation.pre_course not in pre_course_list:
                pre_course_list.append(pre_relation.pre_course)
        # 找到code对应的课程信息
        for pre_course_code in pre_course_list:
            pre_course = Course.query.filter_by(course_code=pre_course_code).order_by(Course.course_name.asc()).first()
            prerequisite_course = {}
            prerequisite_course['course_type'] = pre_course.course_type
            prerequisite_course['course_code'] = pre_course.course_code
            prerequisite_course['course_name'] = pre_course.course_name
            course['prerequisite_course'].append(prerequisite_course)

    # 返回请求结果
    response = {
        'code': "200",
        'info': 'success',
        'result': {
            'course': course_list,
            'search_type': 'all'
        }
    }
    return jsonify(response)


@system.route("/get_student_course_list", methods=['GET'])
@auth.login_required
def get_student_course_list():
    """
    根据student id获取course list
    :return: course list
    """
    stuid = request.args.get('stuid')
    # 获取请求的页码, 默认为 1
    page = request.args.get('page', 1, type=int)

    # 每页展示9个
    per_page = 9

    # 获取请求页码的 course list
    pagination = Taken.query.filter_by(stuid=stuid).order_by(Taken.course_code.asc()).paginate(
        page, per_page=per_page,
        error_out=False
    )

    taken_list_orm = pagination.items

    # 获取总页码数量
    total_page_num = ceil(Taken.query.filter_by(stuid=stuid).count() / per_page)

    # 待返回的course_list
    course_list = []

    # 获取 course code 列表
    # taken_list_orm = Taken.query.filter_by(stuid=stuid).all()
    course_code_list = []
    for taken in taken_list_orm:
        course_code_list.append(taken.course_code)

    # 根据 course code 列表获取课程列表
    for course_code in course_code_list:
        course_orm = Course.query.filter_by(course_code=course_code).first()
        course = {
            'course_code': course_orm.course_code,
            'course_name': course_orm.course_name,
            'course_type': course_orm.course_type,
            'cilo': [],
            'prerequisite_course': []
        }

        # 获取课程的CILO
        cilo_orm_list = CILO.query.filter_by(course_code=course_code).all()
        for cilo_orm in cilo_orm_list:
            course['cilo'].append({
                'cilo_index': cilo_orm.index,
                'cilo_content': cilo_orm.content
            })

        # 获取课程的前置课程的course code list
        pre_course_code_list = []
        pre_orm_list = Pre.query.filter_by(post_course=course_code).all()
        for pre_orm in pre_orm_list:
            if pre_orm.pre_course not in pre_course_code_list:
                pre_course_code_list.append(pre_orm.pre_course)

        pre_course_list = []
        for pre_course_code in pre_course_code_list:
            pre_course_orm = Course.query.filter_by(course_code=pre_course_code).first()
            pre_course = {
                'course_code': pre_course_orm.course_code,
                'course_name': pre_course_orm.course_name,
                'course_type': pre_course_orm.course_type
            }
            pre_course_list.append(pre_course)

        course['prerequisite_course'] = pre_course_list

        course_list.append(course)



        # # 获取课程CILO对应的前置课程 (处理and和or关系)
        # for cilo_orm in cilo_orm_list:
        #
        #     # 初始化type
        #     type = 0
        #
        #     # 拿到这个cilo index对应的所有的pre关系
        #     pre_orm_list = Pre.query.filter_by(post_course=course_code, post_cilo_index=cilo_orm.index).all()
        #
        #     for pre_orm in pre_orm_list:
        #         type += 1
        #         pre_course_code_list = []  # 隶属于同一个or关系的course_code_list
        #         if pre_orm.type == type:
        #             # or关系
        #             pre_course_code_list.append(pre_orm.pre_course)
        #         pre_course_list = []  # 隶属于同一个or关系的course_list
        #         for pre_course_code in pre_course_code_list:
        #             pre_course_orm = Course.query.filter_by(course_code=pre_course_code).first()
        #             pre_course = {
        #                 'code': pre_course_orm.course_code,
        #                 'name': pre_course_orm.course_name,
        #                 'type': pre_course_orm.course_type
        #             }
        #             pre_course_list.append(pre_course)


    return jsonify({
        'code': 200,
        'info': 'query student course list successfully',
        'result': {
            'total_page': total_page_num,
            'courseList': course_list
        }
    })


@system.route("/search_course_for_student", methods=['GET'])
def search_course_for_student():
    """
    通过type和keyword来检索课程
    :return:
    """
    # 请求的页码, 默认为 1
    page = request.args.get('page', 1, type=int)

    # 请求的参数
    keyword = request.args.get('keyword')
    type = request.args.get('type')
    stuid = request.args.get('stuid')

    # page参数
    per_page = 9
    total_page_num = 1

    course_list = []

    if type == 'by keyword':

        # 查询keyword
        cilo_result_list = []

        # 对应的课程
        cilo_orm_list = CILO.query.filter(
            CILO.content.like("%" + keyword + "%") if keyword is not None else ""
        ).all()

        for cilo_orm in cilo_orm_list:
            result = {
                'current': {
                    'cilo_index': '',
                    'cilo_content': '',
                    'course': {
                        'name': '',
                        'code': '',
                        'type': ''
                    }
                },
                'pre': [],
                'post': []
            }

            # 现在查询到的CILO
            result['current']['cilo_index'] = cilo_orm.index
            result['current']['cilo_content'] = cilo_orm.content

            course_code = cilo_orm.course_code

            course_orm = Course.query.filter_by(course_code=course_code).first()
            result['current']['course']['name'] = course_orm.course_name
            result['current']['course']['code'] = course_orm.course_code
            result['current']['course']['type'] = course_orm.course_type

            # 前置CILO
            pre_orm_list = Pre.query.filter_by(post_course=course_code, post_cilo_index=cilo_orm.index)

            for pre_orm in pre_orm_list:
                pre_cilo_orm = CILO.query.filter_by(course_code=pre_orm.pre_course,
                                                    index=pre_orm.pre_cilo_index).first()
                pre = {
                    'cilo_index': pre_orm.pre_cilo_index,
                    'cilo_content': pre_cilo_orm.content,
                    'course': {
                        'name': '',
                        'code': '',
                        'type': ''
                    }
                }
                pre_course_orm = Course.query.filter_by(course_code=pre_orm.pre_course).first()
                pre['course']['name'] = pre_course_orm.course_name
                pre['course']['code'] = pre_course_orm.course_code
                pre['course']['type'] = pre_course_orm.course_type

                result['pre'].append(pre)

            # 后置CILO
            post_orm_list = Pre.query.filter_by(pre_course=course_code, pre_cilo_index=cilo_orm.index)

            for post_orm in post_orm_list:
                post_cilo_orm = CILO.query.filter_by(course_code=post_orm.post_course,
                                                     index=post_orm.post_cilo_index).first()
                post = {
                    'cilo_index': post_orm.post_cilo_index,
                    'cilo_content': post_cilo_orm.content,
                    'course': {
                        'name': '',
                        'code': '',
                        'type': ''
                    }
                }
                post_course_orm = Course.query.filter_by(course_code=post_orm.post_course).first()
                post['course']['name'] = post_course_orm.course_name
                post['course']['code'] = post_course_orm.course_code
                post['course']['type'] = post_course_orm.course_type

                result['post'].append(post)
            cilo_result_list.append(result)

        # 查询course
        current_course_list = []

        pre_course_list = []
        pre_course_code_list = []
        post_course_list = []
        post_course_code_list = []

        # 对应的课程
        name_orm_list = Course.query.filter(
            Course.course_name.like("%" + keyword + "%") if keyword is not None else ""
        ).all()

        code_orm_list = Course.query.filter(
            Course.course_code.like("%" + keyword + "%") if keyword is not None else ""
        ).all()

        # cilo_orm_list = CILO.query.filter(
        #     CILO.content.like("%" + keyword + "%") if keyword is not None else ""
        # ).all()

        current_course_code_list = []  # 对应现在CILO的课程code列表
        # for cilo_orm in cilo_orm_list:
        #     if cilo_orm.course_code not in current_course_code_list:
        #         current_course_code_list.append(cilo_orm.course_code)
        for name_orm in name_orm_list:
            if name_orm.course_code not in current_course_code_list:
                current_course_code_list.append(name_orm.course_code)
        for code_orm in code_orm_list:
            if code_orm.course_code not in current_course_code_list:
                current_course_code_list.append(code_orm.course_code)

        for current_course_code in current_course_code_list:
            course = {
                'course_name': '',
                'course_code': '',
                'course_type': '',
                'cilo': [],
                'prerequisite_course': []
            }
            course_orm = Course.query.filter_by(course_code=current_course_code).first()
            course['course_name'] = course_orm.course_name
            course['course_code'] = course_orm.course_code
            course['course_type'] = course_orm.course_type

            # 获取CILO
            current_course_cilo_list = CILO.query.filter_by(course_code=current_course_code).all()

            for current_course_cilo in current_course_cilo_list:
                course['cilo'].append(current_course_cilo.content)

            # 获取前置
            pre_course_orm_list = Pre.query.filter_by(post_course=current_course_code).all()
            for pre_course_orm in pre_course_orm_list:
                if pre_course_orm.pre_course not in pre_course_code_list:
                    pre_course_code_list.append(pre_course_orm.pre_course)

            for pre_course_code in pre_course_code_list:
                pre_course = Course.query.filter_by(course_code=pre_course_code).first()
                course['prerequisite_course'].append({
                    'course_code': pre_course.course_code,
                    'course_name': pre_course.course_name,
                    'course_type': pre_course.course_type
                })
            current_course_list.append(course)

        return jsonify({
            'code': '200',
            'info': 'search by keyword successfully',
            'search_type': 'by keyword',
            'result': {
                'cilo': cilo_result_list,
                'course': current_course_list
            },
        })

    elif type == 'by Course':

        current_course_code_list = []
        result_list = []

        # 找到对应的课程
        course_list_by_name = Course.query.filter(
            Course.course_name.like("%" + keyword + "%") if keyword is not None else "").all()
        course_list_by_code = Course.query.filter(
            Course.course_code.like("%" + keyword + "%") if keyword is not None else "").all()

        # 把两个list的所有课程放到一起
        for course in course_list_by_name:
            current_course_code_list.append(course.course_code)
        for course in course_list_by_code:
            if course not in current_course_code_list:
                current_course_code_list.append(course.course_code)

        # 对每个搜到的课程都有一组(pre,current,post),所有内容都写在这个循环里边
        for current_course_code in current_course_code_list:
            # 对于每个current course都清空这些信息
            pre_course_code_list = []
            post_course_code_list = []

            course = {
                'name': '',
                'code': '',
                'type': '',
                'CILO': [],
            }

            result = {
                'pre': [],
                'current': course,
                'post': [],
            }

            # 找到这门课程自身的信息
            course_orm = Course.query.filter_by(course_code=current_course_code).first()
            course['name'] = course_orm.course_name
            course['code'] = course_orm.course_code
            course['type'] = course_orm.course_type
            # 获取current course的CILO
            current_course_cilo_list = CILO.query.filter_by(course_code=current_course_code).all()
            for current_course_cilo in current_course_cilo_list:
                course['CILO'].append(current_course_cilo.content)
            result['current'] = course

            # 找到该门课的所有前置课程的course_code
            pre_course_list = Pre.query.filter_by(post_course=current_course_code).all()
            for pre_course in pre_course_list:
                if pre_course.pre_course not in pre_course_code_list:
                    pre_course_code_list.append(pre_course.pre_course)
            print(pre_course_code_list)
            for pre_course_code in pre_course_code_list:
                pre_course_obj = {
                    'name': '',
                    'code': '',
                    'type': '',
                    'CILO': [],
                }
                pre_course = Course.query.filter_by(course_code=pre_course_code).first()
                pre_course_obj['name'] = pre_course.course_name
                pre_course_obj['code'] = pre_course.course_code
                pre_course_obj['type'] = pre_course.course_type

                # 获取CILO
                pre_course_cilo_list = CILO.query.filter_by(course_code=pre_course_code).all()

                for pre_course_cilo in pre_course_cilo_list:
                    pre_course_obj['CILO'].append(pre_course_cilo.content)

                result['pre'].append(pre_course_obj)

            # 找到这门课程所有的后置课程
            post_course_list = Pre.query.filter_by(pre_course=current_course_code).all()
            for post_course in post_course_list:
                if post_course.post_course not in post_course_code_list:
                    post_course_code_list.append(post_course.post_course)

            for post_course_code in post_course_code_list:
                post_course_obj = {
                    'name': '',
                    'code': '',
                    'type': '',
                    'CILO': [],
                }
                post_course = Course.query.filter_by(course_code=post_course_code).first()
                post_course_obj['name'] = post_course.course_name
                post_course_obj['code'] = post_course.course_code
                post_course_obj['type'] = post_course.course_type

                # 获取CILO
                post_course_cilo_list = CILO.query.filter_by(course_code=post_course_code).all()

                for post_course_cilo in post_course_cilo_list:
                    post_course_obj['CILO'].append(post_course_cilo.content)

                result['post'].append(post_course_obj)

            # 现在的result里包含了current course的前置课程名字，自身信息，后置课程名字
            result_list.append(result)
        print(result_list)

        return jsonify({
            'code': '200',
            'info': 'search by course successfully',
            'total_page': 1,
            'search_type': 'by Course',
            'result': result_list
        })


    elif type == 'by CILO':

        index_list = []
        result_list = []

        # 对应的课程
        cilo_orm_list = CILO.query.filter(
            CILO.content.like("%" + keyword + "%") if keyword is not None else ""
        ).all()

        for cilo_orm in cilo_orm_list:
            result = {
                'current': {
                    'cilo_index': '',
                    'cilo_content': '',
                    'course': {
                        'name': '',
                        'code': '',
                        'type': ''
                    }
                },
                'pre': [],
                'post': []
            }

            # 现在查询到的CILO
            result['current']['cilo_index'] = cilo_orm.index
            result['current']['cilo_content'] = cilo_orm.content

            course_code = cilo_orm.course_code

            course_orm = Course.query.filter_by(course_code=course_code).first()
            result['current']['course']['name'] = course_orm.course_name
            result['current']['course']['code'] = course_orm.course_code
            result['current']['course']['type'] = course_orm.course_type

            # 前置CILO
            pre_orm_list = Pre.query.filter_by(post_course=course_code, post_cilo_index=cilo_orm.index)

            for pre_orm in pre_orm_list:
                pre_cilo_orm = CILO.query.filter_by(course_code=pre_orm.pre_course,
                                                    index=pre_orm.pre_cilo_index).first()
                pre = {
                    'cilo_index': pre_orm.pre_cilo_index,
                    'cilo_content': pre_cilo_orm.content,
                    'course': {
                        'name': '',
                        'code': '',
                        'type': ''
                    }
                }
                pre_course_orm = Course.query.filter_by(course_code=pre_orm.pre_course).first()
                pre['course']['name'] = pre_course_orm.course_name
                pre['course']['code'] = pre_course_orm.course_code
                pre['course']['type'] = pre_course_orm.course_type

                result['pre'].append(pre)

            # 后置CILO
            post_orm_list = Pre.query.filter_by(pre_course=course_code, pre_cilo_index=cilo_orm.index)

            for post_orm in post_orm_list:
                post_cilo_orm = CILO.query.filter_by(course_code=post_orm.post_course,
                                                     index=post_orm.post_cilo_index).first()
                post = {
                    'cilo_index': post_orm.post_cilo_index,
                    'cilo_content': post_cilo_orm.content,
                    'course': {
                        'name': '',
                        'code': '',
                        'type': ''
                    }
                }
                post_course_orm = Course.query.filter_by(course_code=post_orm.post_course).first()
                post['course']['name'] = post_course_orm.course_name
                post['course']['code'] = post_course_orm.course_code
                post['course']['type'] = post_course_orm.course_type

                result['post'].append(post)
            result_list.append(result)

        return jsonify({
            'code': '200',
            'info': 'search by cilo successfully',
            'total_page': 1,
            'search_type': 'by CILO',
            'result': result_list
        })

    else:
        pass

    response = {
        'code': "200",
        'info': 'success',
        'result': {
            'total_page': total_page_num,
            'course': course_list,
            'search_type': type
        }
    }
    return jsonify(response)

