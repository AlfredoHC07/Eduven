class Config:
    DEBUG = True
    TESTING = True
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://zjusxcfmfwujtd:bcaa13a0feeb9138b0d8c5a0d0c366bb59e2463b764b9ca246d339b839f288ea@ec2-3-228-235-79.compute-1.amazonaws.com:5432/d102ukg1pnng0u'

class ProductionConfig(Config):
    DEBUG = False
class DevelopmentConfig(Config):
    SECRET_KEY = 'dev'
    DEBUG = True
    TESTING = True