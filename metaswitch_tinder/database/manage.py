from metaswitch_tinder.app import db


def purge_table(table):
    # Delete all rows in specified table
    table.query.delete()
    db.session.commit()


def delete_table(table):
    # Delete specified table
    table.__table__.drop(db.session.bind)
    db.session.commit()
