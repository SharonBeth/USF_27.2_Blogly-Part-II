"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connet to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """Users"""
    
    __tablename__ = 'users'

    # Example from videos
    @classmethod
    def get_user_by_id(cls, id):
        cls.query.filter_by(id=id).all()
    
    # Example from videos
    # def __repr__(self):
        # p = self
        # return f"XXXXXXXX"
    def __repr__(self):
        u = self
        return f"<User id={u.id} first_name ={u.first_name} last_name={u.last_name} image_url={u.image_url}>"
    id          = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True)
    first_name  = db.Column(db.String(25),
                            nullable=True)
    last_name   = db.Column(db.String(25),
                            nullable=True)
    image_url   = db.Column(db.String,
                            nullable=True)
    
    postings = db.relationship('Post', backref ='user', cascade="all, delete-orphan")

class Post(db.Model):
    """Posts"""

    __tablename__ = 'posts'

    def __repr__(self):
        p = self
        return f"<User id={p.id} title={p.title} content={p.content} DateTime={p.created_at} user_id={p.user_id}>"
    
    id          = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True)
    title       = db.Column(db.String,
                            nullable=True)
    content     = db.Column(db.String,
                            nullable=True)
    created_at  = db.Column(db.DateTime,
                            nullable=False, default=datetime.utcnow)
    user_id     = db.Column(db.Integer,
                            db.ForeignKey('users.id'), nullable=False)
                            
    # userid    = db.relationship('User', backref='ids')
     
class PostTag(db.Model):
    """Joining table of Post Model & Tag Model"""

    __tablename__ = 'posts_tags'

    def __repr__(self):
        pt = self
        return f"<Post ID={pt.post_id} Tag ID={pt.tag_id}>"
    
    post_id     = db.Column(db.Integer,
                            db.ForeignKey('posts.id'),
                            primary_key=True,
                            )
    tag_id      = db.Column(db.Integer,
                            db.ForeignKey('tags.id'),
                            primary_key=True)

class Tag(db.Model):
    """Tag Id's"""

    __tablename__ = 'tags'

    def __repr__(self):
        t=self
        return f"<Tag id={t.id} Tag Name={t.name}>"
    
    id          = db.Column(db.Integer,
                            primary_key=True,
                            )
    name        = db.Column(db.String,
                            nullable=True)
    
    posts       = db.relationship('Post',
                                    secondary="posts_tags",
                                    backref="tags")
    

    
