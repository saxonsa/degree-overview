
# database
#HOSTNAME = 'cdb-515vasvh.gz.tencentcdb.com'
HOSTNAME = 'localhost'
#PORT = '10054'
PORT = '3306'
USERNAME = 'root'
#PASSWORD = 'Sa5218588'
PASSWORD = '123'
DATABASE = 'daffodil'

class DebugMode(object):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

    # auto commit
    # SQLALCHEMY_COMMIT_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # secret key
    SECRET_KEY = b'=s\x0e\x04;\xf3\xfaV%z\xf7\x12}\xfe\x86.U\xe6\xe9\xcb\x94\xdc\xda\xa6'
    TOKEN_EXPIRATION = 36000

    TESTING = True
