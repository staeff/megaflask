import datetime

from app import db, models

# create an entry

# get user by id
u = models.User.query.get(1)
p = models.Post(body='First post!', timestamp=datetime.datetime.utcnow(), author=u)
db.session.add(p)
db.session.commit()

# check the results
posts = u.posts.all()
print(posts)