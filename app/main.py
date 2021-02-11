from flask import Flask, request, render_template

app = Flask(__name__)
app.config['DEBUG'] = True

# the form of database uri should be --> dialect+driver://username:password@host:port/database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://POSTGRES_USER:POSTGRES_PASSWORD@db:5432/POSTGRES_DB'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hello_flask:hello_flask@db:5432/hello_flask_dev'

import redis
from flask_migrate import Migrate

from models import db, UserFavs

# manager = Manager(app)
migrate = Migrate(app, db)

# ...app config...
db.init_app(app)
with app.app_context():
    db.create_all()
    db.session.commit()

red = redis.Redis(host='redis', port=6379, db=0)

@app.route("/")
def home():
    return render_template('red.html')

@app.route("/save", methods=['POST'])
def save():
    username = str(request.form['username']).lower()
    place = str(request.form['place']).lower()
    food = str(request.form['food']).lower()

    if red.hgetall(username).keys():
        print("hget username:", red.hgetall(username))
        return render_template('red.html', user_exists=1, msg='(From Redis)', username=username, place=red.hget(username,"place").decode('utf-8'), food=red.hget(username,"food").decode('utf-8'))

    elif len(list(red.hgetall(username)))==0:
        record =  UserFavs.query.filter_by(username=username).first()
        print("Records fecthed from db:", record)
        if record:
            red.hset(username, "place", place)
            red.hset(username, "food", food)
            return render_template('red.html', user_exists=1, msg='(From DataBase)', username=username, place=record.place, food=record.food)

    new_record = UserFavs(username=username, place=place, food=food)
    db.session.add(new_record)
    db.session.commit()

    red.hset(username, "place", place)
    red.hset(username, "food", food)

    record =  UserFavs.query.filter_by(username=username).first()
    print("Again from db:", record)
    print("Again from db: place", type(record.place), record.place)

    print("key-values:", red.hgetall(username))
    print("keys:", red.hkeys(username))
    print("key-values:", red.hvals(username))
    print("Value for place:", red.hget(username, "place"))
    print("Value for food:", red.hget(username, "food"))

    return render_template('red.html', saved=1, username=username, place=red.hget(username, "place").decode('utf-8'), food=red.hget(username, "food").decode('utf-8'))

@app.route("/get", methods=['POST'])
def get():
    username = request.form['username']
    favs = red.hgetall(username)
    print("username", username)
    print("favs type", type(favs), favs)
    print("*******",len(list(favs)))
    if not favs:
        record =  UserFavs.query.filter_by(username=username).first()
        print("Records fecthed from db:", record)
        if not record:
            return render_template('red.html', no_record=1, response=f"Record for '{username}'  not yet defined !")
        red.hset(username, "place", record.place)
        red.hset(username, "food", record.food)
        print(red.hget(username, "place"), red.hget(username, "food"))
        print(record.place, record.food)
        return render_template('red.html', get=1, msg='(From DataBase)', username=record.username, place=record.place, food=record.food)

    return render_template('red.html', get=1, msg='(From Redis)', username=username, place=favs[b'place'].decode('utf-8'), food=favs[b'food'].decode('utf-8'))

@app.route("/keys", methods=['GET'])
def keys():
    all_keys = red.keys("*")
    return render_template('red.html', usernames=all_keys)

@app.route("/hello")
def hello():
    return "Hello World from Flask in a uWSGI Nginx Docker container with \
     Python 3.8 (from the example template)"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=80)
