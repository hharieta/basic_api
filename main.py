import json
from urllib import response
from flask import Flask, jsonify, make_response, render_template, request

app1 = Flask(__name__)

@app1.route('/')
def helloWorld():
    return "Hello World"

@app1.route('/gatovsky')
def helloGatovsky():
    return "Hello, Gatovsky"

@app1.route('/html')
def home():
    return render_template(("index.html"))

@app1.route('/qs')
def get_qs():
    if request.args:
        req = request.args
        return " ".join(f"{k}:{v}" for k, v in req.items())
    
    return "No query"


order = {
    "orden1" : {
        "Size" : "Small",
        "Toppings" : "Cheese",
        "Crust" : "Thin Crust"
    }
}

@app1.route('/orders')
def get_order():
    response = make_response(jsonify(order), 200)
    return response

def main():
    app1.run(debug=True)


if __name__ == '__main__':
    main()
