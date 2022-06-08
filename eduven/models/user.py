from eduven import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(50),unique=True)
    password = db.Column(db.Text)
    fullname = db.Column(db.String(70))
    
    def __init__(self, username, password, fullname) -> None:
        self.username = username
        self.password = password
        self.fullname = fullname

    def __repr__(self) -> str:
        return f'User: {self.username}'

