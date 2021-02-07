from flask import Flask, request, render_template
import redis
from flask_script import Manager
from flask_migrate import Migrate

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hello_flask:hello_flask@db:5432/hello_flask_dev'

from models import db
from models import UserFavs

manager = Manager(app)
migrate = Migrate(app, db)

# ...app config...
db.init_app(app)
with app.app_context():
    db.create_all()
    db.session.commit()

red = redis.Redis(host='redis', port=6379, db=0)

@app.route("/")
def main():
    return render_template('red.html')

@app.route("/save", methods=['POST'])
def save():
    username = str(request.form['username']).lower()
    place = str(request.form['place']).lower()
    food = str(request.form['food']).lower()

    if len(list(red.hgetall(username)))==0:
        records =  UserFavs.query.filter_by(username=username).all()
        print("Records fecthed from db:", records)

    red.hset(username, "place", place)
    red.hset(username, "food", food)

    new_record = UserFavs(username=username, place=place, food=food)
    # new_record = UserFavs(username=username, place=place)
    db.session.add(new_record)
    db.session.commit()

    record =  UserFavs.query.filter_by(username=username).all()
    print("Again from db:", record)

    # red.hset(username, "place", place)
    # red.hset(username, "food", food)

    print("key-values:", red.hgetall(username))
    print("keys:", red.hkeys(username))
    print("key-values:", red.hvals(username))
    print("Value for place:", red.hget(username, "place"))
    print("Value for food:", red.hget(username, "food"))


    # working -----
    # ret_set = red.set(username,place) 
    # ret_set_place = red.get(username).decode('utf-8') 
    # working -----

    # working -----
    # ret_set = red.sadd("vag","asw") 
    # ret_set_place = red.smembers("vag")
    # working -----

    # ret_set_place_old = red.smembers(username)
    # print("Previous places of user:", ret_set_place_old)

    # if place.encode() not in ret_set_place_old:
    #     print("Place not exists till now!")

    # ret_set = red.sadd(username,place,food) 
    # ret_set_place = red.smembers(username)

    print("----------------")
    # print(type(ret_set_place))
    print("----------------")

    return render_template('red.html', saved=1, username=username, place=red.hget(username, "place").decode('utf-8'), food=red.hget(username, "food").decode('utf-8'))
    # return render_template('red.html', saved=1, place=red.hget(username, "place").decode('utf-8'))

@app.route("/get", methods=['POST'])
def get():
    username = request.form['username']
    favs = red.hgetall(username)
    print("favs type", type(favs), favs)
    # if len(list(red.hgetall(username))):
    print("*******",len(list(favs)))
    if len(list(favs))==0:
        record =  UserFavs.query.filter_by(username=username).all()
        print("Records fecthed from db:", records)
        if len(records)==0:
            return render_template('red.html', username=username, place="Not defined yet")
        return render_template('red.html', username=record.username, place=record.place)
    # str_place = place.decode('utf-8')
    # return render_template('red.html', username=username)
    return render_template('red.html', username=username, place=favs[b'place'].decode('utf-8'), food=favs[b'food'].decode('utf-8'))

@app.route("/keys", methods=['GET'])
def keys():
    all_keys = red.keys("*")
    return render_template('red.html', usernames=all_keys)