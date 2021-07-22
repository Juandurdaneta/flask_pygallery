import os
class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql://ftlzeonxpvxopp:125c8fe257455f4d6051a0ae94c540aaefcab3cf222bfb57c894529ecd7ec3ee@ec2-34-193-112-164.compute-1.amazonaws.com:5432/d6fatj18kbqdes'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')