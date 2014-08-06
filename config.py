import os
baseDir = os.path.abspath(os.path.dirname(__file__))



class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    ONLINE_LAST_MINUTES = 3

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    USERNAME = 'cat'
    PASSWORD = '123456'
    SQL_HOST = 'localhost'
    SQL_PORT = ''
    DATABASENAME = 'food'
#    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
#            'sqlite:///' + os.path.join(baseDir, 'data-dev.sqlite')
#    SQLALCHEMY_DATABASE_URI = 'mysql://' + USERNAME + ':' + PASSWORD + \
#            '@' + HOST + ':' + str(PORT) + '/' + DATABASENAME
#    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/FOOD'
    SQLALCHEMY_DATABASE_URI = 'mysql://' + USERNAME + ':' + PASSWORD + \
            '@' + SQL_HOST +  "/" + DATABASENAME
#    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/FOOD'
#    SQLALCHEMY_DATABASE_URI = "mysql://test@121.40.87.145:3306/food"

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
            'sqlite:///' + os.path.join(baseDir, 'data-test.sqlite')

class ProductionConfig(Config):

    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/FOOD'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
                fromaddr=cls.FLASKY_MAIL_SENDER,
                toaddrs=[cls.FLASKY_ADMIN],
                subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error',
                credentials=credentials,
                secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

config = {
        'development' : DevelopmentConfig,
        'testing' : TestingConfig,
        'production' : ProductionConfig,
        'default' : DevelopmentConfig
}
