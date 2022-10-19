from crypt import methods
from datetime import datetime
from enum import unique
import os
from urllib import response
from wsgiref import headers
import requests
import uuid
from flask import Flask, request
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
load_dotenv()

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DB_URL')
db = SQLAlchemy()
db.init_app(app)


class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default= db.func.now())
    updated_at = db.Column(db.DateTime,
        default= db.func.now(),
        onupdate=db.func.now())


class Service(db.Model):
    id = db.Column(db.String, primary_key=True)
    location = db.Column(db.String)
    services = db.Column(db.String)
    created_at = db.Column(db.DateTime, default= db.func.now())
    updated_at = db.Column(db.DateTime,
        default= db.func.now(),
        onupdate=db.func.now())


class Order(db.Model):
    id = db.Column(db.String, primary_key=True)
    service_id = db.Column(db.String, primary_key=True)
    date = db.Column(db.DateTime)
    location = db.Column(db.String)
    services = db.Column(db.String)
    created_at = db.Column(db.DateTime, default= db.func.now())
    updated_at = db.Column(db.DateTime,
        default= db.func.now(),
        onupdate=db.func.now())



# with app.app_context():
#         db.create_all()

@app.route("/cabins/owned", methods=['GET'])
def cabins():
    if request.method == 'GET':
        cabins = requests.get('https://wom22-projekt2-kanjikar-fallstrs.azurewebsites.net/cabins/owned', headers= {"Authorization" :request.headers['Authorization'] })
        return cabins.json()

@app.route("/services", methods=['POST' , 'GET', 'PATCH', 'DELETE'])
def services():

        if request.method == 'GET':
            try:
                services = []
                for service in Service.query.all():
                    services.append({
                    'id': service.id,
                    'location': service.location,
                    'services': service.services,
                    'created_at': service.created_at,
                    'updated_at': service.updated_at
                    })

                return services
            except: return {'msg': "Pass"}

        if request.method == 'POST':
            try:    
                body = request.get_json()

                new_service = Service(
                    id = str(uuid.uuid4()),
                    location = body['location'],
                    services = body['service']
                    )

                db.session.add(new_service)
                db.session.commit()

                return {'msg': 'Service created', 'id': new_service.id}
            except: return {'msg': "Pass"}

        if request.method == 'DELETE':
            try:        
                body = request.get_json()
                Service.query.filter_by(id = body['id']).delete()
            
                db.session.commit()

                return {'msg': 'Service deleted', 'id': body['id']}
            except: return {'msg': "Pass"}

        if request.method == 'PATCH': 
            try: 
                body = request.get_json()
                service = Service.query.filter_by(id = body['id']).first()
                service.location = body['location'],
                service.services = body['service']
                db.session.commit()
                return {'msg': 'Service updated', 'location': body['location']}
            except: return {'msg': "Pass"}

   

@app.route("/orders", methods=['GET', 'POST', 'PATCH', 'DELETE'])
def orders():
    if request.method == 'GET':
        try: 
            orders = []
            for order in Order.query.all():
                orders.append({
                    'id': order.id,
                    'date': order.date,
                    'service_id': order.service_id,
                    'location': order.location,
                    'services': order.services,
                    'created_at': order.created_at,
                    'updated_at': order.updated_at
                    })
            return orders
        except: return {'msg': "Pass"}

    if request.method == 'POST':
        try: 
            body = request.get_json()
            new_order = Order(
                id = str(uuid.uuid4()),
                service_id = body['service_id'],
                date = body['date'],
                location = body['location'],
                services = body['service']
                )

            db.session.add(new_order)
            db.session.commit()

            return {'msg': 'Order created', 'id': new_order.id}
        except: return {'msg': "Pass"}

    if request.method == 'DELETE':
        try: 
            body = request.get_json()
            Order.query.filter_by(id = body['id']).delete()
            db.session.commit()
            return {'msg': 'Order deleted', 'id': body['id']}
        except: return {'msg': "Pass"}

    if request.method == 'PATCH':
        try: 
            body = request.get_json()
            
            order = Order.query.filter_by(id = body['id']).first()

            order.date = body['date'],
            order.location = body['location'],
            order.services = body['service']

            db.session.commit()

            return {'msg': 'Order updated'}
        except: return {'msg': "Pass"}



@app.route("/", methods=['GET', 'POST'])
def index():
    
    if request.method == 'GET':
        try: 
            return { 
                'method': request.method,
                'msg': 'Github webhook deployment works!', 
                'env': os.environ.get('ENV_VAR', 'Cannot find variable ENV_VAR')
            }
        except: return {'msg': "Pass"}
    if request.method == 'POST':
        try: 
            body = request.get_json()

            return {
                'msg': 'You POSTed something',
                'request_body': body
            }
        except: return {'msg': "Pass"}



@app.route("/users/login", methods=['POST'])
def users():
    
    if request.method == 'POST':
        try:
            body = request.get_json()
            users = requests.post('https://wom22-projekt2-kanjikar-fallstrs.azurewebsites.net/users/login', json = {'email': body['email'], 'password': body['password']})
            print(users.json())
            return users.json()
        except: return {'msg': "Pass"}

# @app.route("/users", methods=['GET', 'POST'])
# def users():
#     if request.method == 'GET':
#         users = []
#         for user in User.query.all():
#             users.append({
#             'id': user.id,
#             'email': user.email,
#             'created_at': user.created_at,
#             'updated_at': user.updated_at
#          })
#       return users
    
#     if request.method == 'POST':
#         body = request.get_json()
#         new_user = User(email = body['email'], id = str(uuid.uuid4()))
#         db.session.add(new_user)
#         db.session.commit()

#         return {'msg': 'User created', 'id': new_user.id}


if __name__ == "__main__":
    app.run(debug=True, port=8080, host='0.0.0.0')
