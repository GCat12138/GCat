import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SMS_ACCOUNT = "cf_weimeishi"
SMS_PASSWORD = "GypbZU"
SMS_URL = 'http://106.ihuyi.cn/webservice/sms.php?method=Submit&account=' + \
        SMS_ACCOUNT + '&password=' + SMS_PASSWORD
