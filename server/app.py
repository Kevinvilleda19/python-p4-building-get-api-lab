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

# GET /bakeries: Returns a list of JSON objects for all bakeries
@app.route('/bakeries', methods=['GET'])
def bakeries():
    bakeries = Bakery.query.all()
    bakeries_list = [bakery.to_dict() for bakery in bakeries]  # Serialize the results
    return jsonify(bakeries_list), 200

# GET /bakeries/<int:id>: Returns a single bakery with its baked goods nested in a list
@app.route('/bakeries/<int:id>', methods=['GET'])
def bakery_by_id(id):
    bakery = Bakery.query.get(id)  # Fetch the bakery by its ID
    if bakery:
        bakery_dict = bakery.to_dict(rules=('baked_goods',))  # Include baked goods in the result
        return jsonify(bakery_dict), 200
    else:
        return jsonify({'error': 'Bakery not found'}), 404

# GET /baked_goods/by_price: Returns a list of baked goods sorted by price in descending order
@app.route('/baked_goods/by_price', methods=['GET'])
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()  # Sort by price descending
    baked_goods_list = [good.to_dict() for good in baked_goods]  # Serialize the results
    return jsonify(baked_goods_list), 200

# GET /baked_goods/most_expensive: Returns the single most expensive baked good
@app.route('/baked_goods/most_expensive', methods=['GET'])
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()  # Get the most expensive baked good
    if most_expensive:
        return jsonify(most_expensive.to_dict()), 200
    else:
        return jsonify({'error': 'No baked goods found'}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)
