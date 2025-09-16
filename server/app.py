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

# REMOVED methods parameter (GET is default)
@app.route('/bakeries')
def get_bakeries():
    bakeries = Bakery.query.all()
    bakeries_data = [bakery.to_dict() for bakery in bakeries]
    return jsonify(bakeries_data)

# REMOVED methods parameter
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)
    
    # Create bakery dictionary with nested baked goods
    bakery_dict = bakery.to_dict()
    bakery_dict['baked_goods'] = [bg.to_dict() for bg in bakery.baked_goods]
    
    return jsonify(bakery_dict)

# REMOVED methods parameter
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    # Sort by price in descending order
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_data = [bg.to_dict() for bg in baked_goods]
    return jsonify(baked_goods_data)

# REMOVED methods parameter
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    # Get the most expensive baked good (highest price)
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    
    if most_expensive:
        return jsonify(most_expensive.to_dict())
    else:
        return jsonify({'error': 'No baked goods found'}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)