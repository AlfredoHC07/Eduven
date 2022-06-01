from datetime import date
from eduven import db

class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    objectt = db.Column(db.String(50))
    description = db.Column(db.Text)
    state = db.Column(db.String(20))
    create = db.Column(db.String(20), nullable=False, default=date.today())
    
    def __init__(self, author, objectt, description, state) -> None:
        self.author = author
        self.objectt = objectt
        self.description = description
        self.state = state

    def __repr__(self) -> str:
        return f'Inventory: {self.objectt}'
    
    
    
