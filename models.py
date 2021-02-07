from flask_sqlalchemy import SQLAlchemy
import datetime
# from app import app
# db = SQLAlchemy(app)
db = SQLAlchemy()


# db.create_all()
# db.session.commit()

# class BaseModel(db.Model):
#     """Base data model for all objects"""
#     __abstract__ = True

#     def __init__(self, *args):
#         super().__init__(*args)

#     def __repr__(self):
#         """Define a base way to print models"""
#         return '%s(%s)' % (self.__class__.__name__, {
#             column: value
#             for column, value in self._to_dict().items()
#         })

#     def json(self):
#         """
#                 Define a base way to jsonify models, dealing with datetime objects
#         """
#         return {
#             column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
#             for column, value in self._to_dict().items()
#         }


# class UserFavs(BaseModel, db.Model):
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