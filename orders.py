from crypt import methods
from urllib import response
from flask import Flask, render_template, make_response, jsonify, request

app = Flask(__name__)

order = {
    "1" : {
        "Size" : "Small",
        "Toppings" : "Cheese",
        "Crust" : "Thin Crust"
    },
    "2" : {
        "Size" : "Medium",
        "Toppings" : "Pepperoni",
        "Crust" : "Thick Crust"
    }
}

@app.route('/orders')
def get_order():
    response = make_response(jsonify(order), 200)
    return response


# Order details using order id
@app.route('/orders/<orderid>')
def get_order_details(orderid):
    if orderid in order:
        response = make_response(jsonify(order[orderid]), 200)
        return response
    
    return "Order no found"

# items details in orders
@app.route('/orders/<orderid>/<item>')
def get_item_details(orderid, item):
    items = order[orderid]

    if item in items:
        response = make_response(jsonify(items[item]), 200)
        return response
    
    return "Item not found"

# create new orders (POST method)
@app.route('/orders/<orderid>/', methods=['POST'])
def post_order_details(orderid):
    req = request.get_json()
    if orderid in order:
        response = make_response(jsonify({'error' : 'Order ID already exists'}), 400)
        return response
    order.update({orderid:req})
    response = make_response(jsonify({'messsage' : 'New order created'}), 201)
    
    return response


# create or update orders (PUT method)
@app.route('/orders/<orderid>', methods=['PUT'])
def put_order_details(orderid):
    req = request.get_json()
    if orderid in order:
        order[orderid] = req
        response = make_response(jsonify({'message' : 'Order Updated'}), 200)

        return response
    order.update({orderid:req})
    response = make_response(jsonify({'message' : 'New order created'}), 201)

    return response

# update only items inside an order or create new order
@app.route('/orders/<orderid>', methods=['PATCH'])
def patch_order_details(orderid):
    req = request.get_json()
    if orderid in order:
        for key, value in req.items():
            order[orderid][key] = value
        response = make_response(jsonify({'message' : 'Oder updated'}), 200)
        return response
    order.update({orderid:req})
    response = make_response(jsonify({'message' : 'New order created'}), 201)

    return response

# delete orders
@app.route('/orders/<orderid>', methods=['DELETE'])
def delete_order_details(orderid):
    if orderid in order:
        del order[orderid]
        # no se refleja el response en postman
        response = make_response(jsonify({'message' : 'Order has been deleted'}), 204)
        return response
    
    response = make_response(jsonify({'error' : 'Order not found'}), 404)

    return response

def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()