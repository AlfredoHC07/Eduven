# from sqlalchemy import Column,String,Integer
# from db import Base, engine
import psycopg2

class Usuario:
    # __tablename__ = 'users'
    # id = Column(Integer, autoincrement=True, primary_key=True)
    # user_name = Column(String(20),unique=True)
    # password = Column(String(16))
    # full_name = Column(String(70))
    def user_res(db, user):
        cursor = db.cursor()
        consulta = "users(user_name, password, full_name)"
        
        try:
            sql = f'INSERT INTO {consulta} VALUES{user};'
            
            cursor.execute(sql)
            
            db.commit()
                
        except Exception as ex:
            print(ex)
    
    def user_logg(db, user_post):
        cursor = db.cursor()  
        
        try:
            sql = """ SELECT id, user_name, password, full_name FROM users
                    WHERE user_name = '{}' """.format(user_post)
                    
            cursor.execute(sql)
                
            user_logged = cursor.fetchone()
            
            if user_logged:
                user = (user_logged[1],user_logged[2],user_logged[3])
                return user
            else:
                return user_logged
                
        except Exception as ex:
            print(ex)
            
    # def get_by_id(db, id):
    #     try:
    #         cursor = db.cursor() 
    #         sql = "SELECT id, username, fullname FROM user WHERE id = {}".format(id)
    #         cursor.execute(sql)
    #         row = cursor.fetchone()
    #         if row != None:
    #             return User(row[0], row[1], None, row[2])
    #         else:
    #             return None
    #     except Exception as ex:
    #         raise Exception(ex)
    
# Base.metadata.create_all(engine)
    
    
    
