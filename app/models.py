from hashlib import md5
from app import db

# Note that we are not declaring this table as a model.
# Since this is an auxiliary table that has no data other than the foreign
# keys, we use the lower level APIs in flask-sqlalchemy to create the
# table without an associated model.
followers =db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
)


class User(db.Model):
    """ Represents the user """
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    # virtual field to help with relationships
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    followed = db.relationship('User',
                                secondary=followers,
                                primaryjoin=(followers.c.follower_id == id),
                                secondaryjoin=(followers.c.followed_id == id),
                                backref=db.backref('followers', lazy='dynamic'),
                                lazy='dynamic')

    # Is a static method, since it this operation does not apply to any
    # particular instance of the class.
    @staticmethod
    def make_unique_nickname(nickname):
        """ Checks if nickname already exists in DB. If so appends number
        to nickname and checks again until nickname does not exists in DB.
        Returns this nickname. """
        if User.query.filter_by(nickname=nickname).first() is None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname = str(version)
            if User.query.filter_by(nickname=new_nickname).first() is None:
                break
            version += 1
        return new_nickname

    """ is_authenticated, is_active, is_anonymous, get_id are classes
    for Flask-Login """

    def is_authenticated(self):
        """ returns True for users unless they are not
        allowed to authenticate for some reason"""
        return True

    def is_active(self):
        """ returns True for users unless they are inactive,
        for example because they have been banned."""
        return True

    def is_anonymous(self):
        """ returns True for users that are not supposed
        to log in."""
        return False

    def get_id(self):
        """ returns a unique identifier for the user in unicode"""
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=wavatar&s=%d' % \
             (md5(self.email.encode('utf-8')).hexdigest(), size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        """  Takes the followed relationship query, which returns all
        the (follower, followed) pairs followed by user. Filter it by the
        followed user. The followed relationship has a lazy mode of dynamic.
        Its not the result of the query, its the actual query object 
        before execution. """
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        return Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id).order_by(
                    Post.timestamp.desc())

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Post(db.Model):
    """ Represents blog posts written by users
        models.Post(body='my first post!',
                    timestamp=datetime.datetime.utcnow(),
                    author=<userobject>)
    """
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
