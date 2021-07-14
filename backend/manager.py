from flask_script import Manager
from app import app
from flask_migrate import Migrate, MigrateCommand
from models.base import db

manager = Manager(app)

# 1. 要使用flask_migrate 必须绑定app 和 db
migrate = Migrate(app, db)
# 2. 把migrateCommand命令添加到manager中
manager.add_command('db', MigrateCommand)

# 创建python manage.py createdb命令，创建数据库
@manager.command
def createdb():
    db.create_all(app=app)
    return '创建数据库成功'


@manager.command
def dropdb():
    db.drop_all()
    return '删除数据库成功'


if __name__ == '__main__':
    # dropdb()
    createdb()
    manager.run()