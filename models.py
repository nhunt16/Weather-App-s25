from client import db


class User(db.Model):
    __tablename__ = "User"

    uid = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String)

class Locations(db.Model):
    __tablename__ = "Locations"

    l_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location = db.Column(db.String)

class UserLocations(db.Model):
    __tablename__ = "UserLocations"

    x = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer)
    l_id = db.Column(db.Integer)
    current = db.Column(db.Boolean)
    
class Temperature(db.Model):
    __tablename__ = "Temperature"

    l_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    t0 = db.Column(db.Float, unique=False, nullable=True)
    t1 = db.Column(db.Float, unique=False, nullable=True)
    t2 = db.Column(db.Float, unique=False, nullable=True)
    t3 = db.Column(db.Float, unique=False, nullable=True)
    t4 = db.Column(db.Float, unique=False, nullable=True)
    t5 = db.Column(db.Float, unique=False, nullable=True)
    t6 = db.Column(db.Float, unique=False, nullable=True)
    t7 = db.Column(db.Float, unique=False, nullable=True)
    t8 = db.Column(db.Float, unique=False, nullable=True)
    t9 = db.Column(db.Float, unique=False, nullable=True)
    t10 = db.Column(db.Float, unique=False, nullable=True)
    t11 = db.Column(db.Float, unique=False, nullable=True)
    t12 = db.Column(db.Float, unique=False, nullable=True)
    t13 = db.Column(db.Float, unique=False, nullable=True)
    t14 = db.Column(db.Float, unique=False, nullable=True)
    t15 = db.Column(db.Float, unique=False, nullable=True)
    t16 = db.Column(db.Float, unique=False, nullable=True)
    t17 = db.Column(db.Float, unique=False, nullable=True)
    t18 = db.Column(db.Float, unique=False, nullable=True)
    t19 = db.Column(db.Float, unique=False, nullable=True)
    t20 = db.Column(db.Float, unique=False, nullable=True)
    t21 = db.Column(db.Float, unique=False, nullable=True)
    t22 = db.Column(db.Float, unique=False, nullable=True)
    t23 = db.Column(db.Float, unique=False, nullable=True)

    time = db.Column(db.String, unique=False, nullable=True)

class Humidity(db.Model):
    __tablename__ = "Humidity"

    l_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    h0 = db.Column(db.Float, unique=False, nullable=True)
    h1 = db.Column(db.Float, unique=False, nullable=True)
    h2 = db.Column(db.Float, unique=False, nullable=True)
    h3 = db.Column(db.Float, unique=False, nullable=True)
    h4 = db.Column(db.Float, unique=False, nullable=True)
    h5 = db.Column(db.Float, unique=False, nullable=True)
    h6 = db.Column(db.Float, unique=False, nullable=True)
    h7 = db.Column(db.Float, unique=False, nullable=True)
    h8 = db.Column(db.Float, unique=False, nullable=True)
    h9 = db.Column(db.Float, unique=False, nullable=True)
    h10 = db.Column(db.Float, unique=False, nullable=True)
    h11 = db.Column(db.Float, unique=False, nullable=True)
    h12 = db.Column(db.Float, unique=False, nullable=True)
    h13 = db.Column(db.Float, unique=False, nullable=True)
    h14 = db.Column(db.Float, unique=False, nullable=True)
    h15 = db.Column(db.Float, unique=False, nullable=True)
    h16 = db.Column(db.Float, unique=False, nullable=True)
    h17 = db.Column(db.Float, unique=False, nullable=True)
    h18 = db.Column(db.Float, unique=False, nullable=True)
    h19 = db.Column(db.Float, unique=False, nullable=True)
    h20 = db.Column(db.Float, unique=False, nullable=True)
    h21 = db.Column(db.Float, unique=False, nullable=True)
    h22 = db.Column(db.Float, unique=False, nullable=True)
    h23 = db.Column(db.Float, unique=False, nullable=True)

    time = db.Column(db.String, unique=False, nullable=True)
