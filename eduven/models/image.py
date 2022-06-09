from eduven import db

class Image(db.Model):
    __tablename__ = 'image_user'
    id     = db.Column(db.Integer, autoincrement=True, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image  = db.Column(db.LargeBinary)
    filename = db.Column(db.String)
    
    def __init__(self, author, image, filename) -> None:
        self.author = author
        self.image = image
        self.filename = filename

    def __repr__(self) -> str:
        return f'Image: {self.image}'