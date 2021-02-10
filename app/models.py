from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class UserFavs(db.Model):
    """Model for the stations table"""
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