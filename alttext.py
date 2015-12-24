from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

# Init
app = Flask(__name__)
db_filename = 'wewlad.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{0}'.format(db_filename)
db = SQLAlchemy(app)
db.create_all()

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('link_id', db.Integer, db.ForeignKey('link.id'))
)

class Link(db.Model):
    __tablename__ = "link"
    id         = db.Column(db.Integer, primary_key=True)
    title      = db.Column(db.String(80), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tags = db.relationship('Tag', secondary=tags, backref=db.backref('links', lazy='dynamic'))

    def __init__(self, link, title):
        self.link = link
        self.title = title

class Tag(db.Model):
    __tablename__ = "tag"
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name


@app.route('/')
def index():
    return 'Todo', 200

@app.route('/all', methods=['GET'])
def all_links():
    return 'Todo', 200

@app.route('/add', methods=['POST'])
def add_link():
    print request.json
    return 'Todo', 200

@app.route('/remove/<int:id>', methods=['POST'])
def remove_link(id):
    print id
    return 'Todo', 200

if __name__ == '__main__':
    app.run()
