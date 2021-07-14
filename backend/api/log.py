import os


def write_txt_file(course_code, course_name, program, log) -> bool:
    """
    :param course_code: 课程代码
    :param course_name: 课程名称
    :param program: 课程所属program
    :param log: operation log
    :return: 创建成功或者失败
    """

    # log文件夹路径
    log_path = os.getcwd().replace('\\', '/') + '/log/'

    # 去除 program 中可能存在的空格
    program = program.replace(' ', '_')

    # program子文件夹路径
    program_path = log_path + program + '/'

    # 去除 course name 中的空格
    course_name = course_name.replace(' ', '_')

    try:

        if not os.path.exists(log_path):
            os.makedirs(log_path)

        if not os.path.exists(program_path):
            os.makedirs(program_path)

        # 课程log文件夹路径
        file = open(program_path + course_code + '_' + course_name + '.txt', 'a')

        file.write(log)

        file.close()

        return True

    except:
        return False

