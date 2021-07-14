from models.lecturer import Lecturer


def check_designer_authority(staffid: str) -> bool:
    # 找到 staff id 对应的 staff
    lecturer = Lecturer.query.filter_by(staffid=staffid).first()
    if lecturer is None:
        return False
    else:
        if lecturer.get_design_auth() == 1:
            return True
        else:
            return True
