from app import db, models


# Create two users
u = models.User(nickname='john', email='john@email.com')
db.session.add(u)
db.session.commit()

u = models.User(nickname='susan', email='susan@email.com')
db.session.add(u)
db.session.commit()

# get the users
users = models.User.query.all()
print(users)


# query user by id
u = models.User.query.get(1)
print(u)