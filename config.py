import os
baseDir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    USERNAME = 'root'
    PASSWORD = 'root'
#    HOST = 'localhost'
#    PORT = 8889
    DATABASENAME = 'FOOD'
#    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
#            'sqlite:///' + os.path.join(baseDir, 'data-dev.sqlite')
#    SQLALCHEMY_DATABASE_URI = 'mysql://' + USERNAME + ':' + PASSWORD + \
#            '@' + HOST + ':' + str(PORT) + '/' + DATABASENAME
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/FOOD'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
            'sqlite:///' + os.path.join(baseDir, 'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(baseDir, 'data.sqlite')

config = {
        'development' : DevelopmentConfig,
        'testing' : TestingConfig,
        'production' : ProductionConfig,
        'default' : DevelopmentConfig
}
