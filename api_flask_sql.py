from crypt import methods
from flask import Flask, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myapp.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class App(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(500))
    toppings = db.Column(db.String(500))
    crust = db.Column(db.String(500))


class AppSchema(ma.Schema):
    class Meta:
        fields = ('order_id', 'size', 'toppings', 'crust')

app_schema = AppSchema(many=True)


@app.route('/')
def hello_world():
    return 'Hello World!'


# CREATE
@app.route('/order', methods = ['POST'])
def post_order():
    req = request.get_json()
    order_id = req["order_id"]
    size = req["size"]
    toppings = req["toppings"]
    crust = req["crust"]

    new_entry = App(order_id = order_id, size = size, toppings = toppings, crust = crust)

    db.session.add(new_entry)
    db.session.commit()

    return redirect(url_for('get_order'))


# READ
@app.route('/order')
def get_order():
    entries = App.query.all()
    result = app_schema.dump(entries)

    return jsonify(result)


# UPDATE
@app.route('/order/<order_id>', methods = ['PUT'])
def update_order(order_id):
    req = request.get_json()
    entry = App.query.get(order_id)
    entry.size = req["size"]
    entry.toppings = req["toppings"]
    entry.crust = req["crust"]

    db.session.add(entry)
    db.session.commit()

    return redirect(url_for("get_order"))


# DELETE
@app.route('/order/<order_id>', methods = ['DELETE'])
def delete_order(order_id):
    T = "deleted"
    F = "imposible delete it. Item not found"

    try:
        entry = App.query.get(order_id)
        db.session.delete(entry)
        db.session.commit()
    except:
        pass
    finally:
        return T if entry else F


if __name__ == '__main__':
    db.create_all()
    app.run()