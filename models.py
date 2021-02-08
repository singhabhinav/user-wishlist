from flask_sqlalchemy import SQLAlchemy
import datetime
# from app import app
# db = SQLAlchemy(app)
db = SQLAlchemy()

# db.create_all()
# db.session.commit()

class UserFavs(db.Model):
    """Model for the stations table"""
    # __tablename__ = 'userplaces'

    # id = db.Column(db.Integer)
    username = db.Column(db.String, primary_key = True)
    place = db.Column(db.String)
    food = db.Column(db.String)

    def __init__(self, username, place, food):
        self.username=username
        self.place=place
        self.food=food


    def __repr__(self):
        """Define a base way to print models"""
        return f"<USer-Place {self.username} {self.place} {self.food}>"