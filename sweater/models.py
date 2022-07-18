from flask_login import UserMixin

from sweater import db, manager


# class User(db.Model, UserMixin):
#     __tablename__ = 'user'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#     email = db.Column(db.String(50))
#     password = db.Column(db.String(50))
#     about = db.Column(db.Text)
#     cond = db.Column(db.Integer)
#     pict = db.Column(db.Integer)
#
#     def __repr__(self):
#         return self.id

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    cond = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return self.id



@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    about = db.Column(db.Text)
    the_date = db.Column(db.DateTime)
    owner = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    def __repr__(self):
        return self.id