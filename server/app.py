#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakers= []
    bakery= Bakery.query.all()
    for bake in bakery:
        bake_dict= {
            "id": bake.id,
            "name": bake.name,
            "created_at": bake.created_at,
            "updated_at": bake.updated_at
        }
        bakers.append(bake_dict)
    # bake_dict= bakery.to_dict()
    response= make_response(jsonify(bakers), 200, {"Content-Type": "application/json"})
    return response
    

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    baker_by_id= Bakery.query.filter(Bakery.id==id).first()
    if not baker_by_id:
        return make_response({"error":"No bakery with that ID"},404)
    else:
        response= make_response(jsonify(baker_by_id.to_dict()), 200)
        return response
    

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    all_prices= []
    prices= BakedGood.query.order_by(BakedGood.price.desc()).all()
    for price in prices:
        baked_good_dict= {
            "id": price.id,
            "name": price.name,
            "price": price.price,
        }
        all_prices.append(baked_good_dict)
    respose= make_response(jsonify(all_prices), 200)
    return respose

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    # all_goods= []
    goods= BakedGood.query.order_by(BakedGood.price.desc()).first()
    # for good in goods:
    good_dict= goods.to_dict()
    # all_goods.append(good_dict)
    response= make_response(jsonify(good_dict), 200)
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)