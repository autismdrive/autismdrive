from random import randint

from app import db


# Generates a random integer for use as ids for users, participants and the like
# where we want to avoid incremental ids that might be easy to guess.
# The context here is passed in by SQL Alchemy and allows us to check details of
# the query to make sure the id doesn't exist, though this is highly unlikely.
def random_integer(context):
    min_ = 100
    max_ = 1000000000
    rand = randint(min_, max_)

    # possibility of same random number is very low.
    # but if you want to make sure, here you can check id exists in database.
    while db.session.query(context.current_column.table).filter(id == rand).limit(1).first() is not None:
        rand = randint(min_, max_)

    return rand