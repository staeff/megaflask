from app import db, models

users = []

u1 = models.User(nickname='john', email='john@example.com')
users.append(u1)
u2 = models.User(nickname='susan', email='susan@example.com')
users.append(u2)
u3 = models.User(nickname='lalala', email='hilfsstoff@googlemail.com')
users.append(u3)

for u in users:
    db.session.add(u)

db.session.commit()

for u in range(len(users)):
    for f in range(len(users)):
        fol = users[u].follow(users[f])
        db.session.add(fol)

db.session.commit()
