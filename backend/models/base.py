from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from contextlib import contextmanager

db = _SQLAlchemy(query_class=BaseQuery)


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield  # 上文执行后会继续往下执行
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


class Base(db.Model):
    __abstract__ = True # 抽象类型, 不会创建实体表

    # 设置对象返回字典的值(value), 同样是所有实例通用的方法，所以放在Base类中
    def __getitem__(self, item):
        return getattr(self, item)

    # 设置列属性的方法(所有实例共有)
    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)


