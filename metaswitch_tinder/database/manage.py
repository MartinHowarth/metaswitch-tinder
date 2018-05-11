from metaswitch_tinder.global_config import DATABASE as db

class User(db.Model):
    name = db.Column(db.String(80), primary_key=True)
    email = db.Column(db.String(120), unique=True)
    bio = db.Column(db.String(2000))
    tags = db.Column(db.String(2000))

    def __init__(self, name, email, bio, tags):
        self.name = name
        self.email = email
        self.bio = bio
        self.tags = tags

    def __repr__(self):
        return """
            Name - %s
              Email - %s
              
              Bio - %s
              
              Tags - %s
            """ % (self.name, self.email, self.bio, self.tags)

    def add(self):
        db.session.add(self)
        db.session.commit()
        return


def list_all_users():
    return User.query.all()

def get_user(match_name):
    return User.query.filter_by(name=match_name).first()

def delete_table(table):
    table.__table__.drop(db.session.bind)
    db.session.commit()
    return

db.create_all()

