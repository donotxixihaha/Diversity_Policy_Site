from flask import Flask
from flask_msearch import Search
from flask_sqlalchemy import SQLAlchemy

# setting of postgreSQL database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://fcjcveutbexema:efa00a6e181ba6f2a6c5af034a7e81a5b099d7c7340812e96719c8c22cd15390@ec2-54-83-55-125.compute-1.amazonaws.com:5432/df9hbd55p7h8d7'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['WHOOSH_BASE'] = 'whoosh'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_POOL_SIZE'] = 15
db = SQLAlchemy(app)

class policies(db.Model):

    # connect to the postgreSQL database table
    __tablename__ = 'policies'
    # can add different variables in __searchable__ parameter for searching
    __searchable__ = ['title','school','abstract']

    id = db.Column(db.Integer,primary_key=True)
    timestamp = db.Column(db.Text)
    title = db.Column(db.Text)
    school = db.Column(db.Text)
    department = db.Column(db.Text)
    administrator = db.Column(db.Text)
    author = db.Column(db.Text)
    state = db.Column(db.Text)
    city = db.Column(db.Text)
    latitude = db.Column(db.Text)
    longitude = db.Column(db.Text)
    link = db.Column(db.Text)
    published_date = db.Column(db.String)
    tags = db.Column(db.Text)
    abstract = db.Column(db.Text)
    text = db.Column(db.Text)

    def __repr__(self):
        return '<Post:{}>'.format(self.title)

# using search package function of msearch
search = Search()
search.init_app(app)

# currently gets 100 results--will need to figure out a way to get best number of potentially useful results
def search(query, filter=None):
    results = policies.query.msearch(query)
    db.session.remove()
    if(filter==None or len(filter)==0):
        return results
    dates = set()
    schools = set()
    for f in filter:
        if(f[0].isdigit()):
            dates.add(f)
        else:
            schools.add(f)
    if(dates==None or len(dates)==0):
        return results.filter(policies.school.in_(schools))
    elif(schools==None or len(schools)==0):
        return results.filter(policies.published_date.in_(dates))
    else:
        return results.filter((policies.school.in_(schools)&policies.published_date.in_(dates)))

# Functions similarly to search(), except results are found using prefix, only searching over title field, and object
# is used differently than the search() object is in the function calling search_suggest()

def search_suggest(query):
    results = policies.query.msearch(query)
    db.session.remove()
    return results
