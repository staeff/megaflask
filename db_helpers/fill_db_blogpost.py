import datetime

from app import db, models

# create entries

posts = ["Tempor anim dolore reprehenderit sit nisi cupidatat exercitation.",
    "Eu consectetur irure eiusmod culpa enim ipsum et dolore labore.",
    "Irure anim voluptate duis anim amet.",
    "Non ad deserunt aliquip elit irure duis officia do ea.",
    "Aute et duis deserunt elit id voluptate sit irure magna incididunt est sit anim ullamco."]

# get user by id
u = models.User.query.get(4)
for post in posts:
    p = models.Post(body=post, timestamp=datetime.datetime.utcnow(), author=u)
    db.session.add(p)
db.session.commit()

# check the results
posts = u.posts.all()
print(posts)
