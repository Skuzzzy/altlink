from flask import Flask, request, render_template, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import json

# Init
app = Flask(__name__)
db_filename = 'wewlad.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{0}'.format(db_filename)
db = SQLAlchemy(app)

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('link_id', db.Integer, db.ForeignKey('link.id'))
)

class Link(db.Model):
    __tablename__ = "link"
    id         = db.Column(db.Integer, primary_key=True)
    title      = db.Column(db.String(80), index=True)
    link       = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tags = db.relationship('Tag', secondary=tags,
                           backref=db.backref('links', lazy='dynamic'))

    def __init__(self, link, title):
        self.link = link
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title,
                "title": self.title,
                "link": self.link,
                "created_at": str(self.created_at),
                "tags": [tag.name for tag in self.tags]}


class Tag(db.Model):
    __tablename__ = "tag"
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

def dict_contains(dictionary, *pargs):
    for each in pargs:
        if not each in dictionary:
            return False
    return True


@app.route('/')
def index():
    return render_template('index.html'), 200

@app.route('/all', methods=['GET'])
def all_links():
    all_links = Link.query.all()
    return json.dumps([link.to_dict() for link in all_links], sort_keys=True, indent=4), 200

@app.route('/add', methods=['POST'])
def add_link():
    if not dict_contains(request.json, "link", "title"):
        return 'Invalid JSON Doc', 400
    new_link = Link(request.json.get("link"), request.json.get("title"))
    db.session.add(new_link)
    db.session.commit()
    return redirect(url_for('all_links'))
    # return 'Created link id:{0}'.format(new_link.id), 200

@app.route('/del/<int:link_id>', methods=['POST'])
def remove_link(link_id):
    to_delete = Link.query.filter_by(id=link_id).first_or_404()
    db.session.delete(to_delete)
    db.session.commit()
    return 'Great Success', 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
