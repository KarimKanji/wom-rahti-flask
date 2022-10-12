from crypt import methods
from enum import unique
import os
from turtle import update
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


# class Order(db.Model):
#     id = db.Column(db.String, primary_key=True)
#     service_id = db.Column(db.String, primary_key=True)
#     location = db.Column(db.String)
#     services = db.Column(db.String)
#     created_at = db.Column(db.DateTime, default= db.func.now())
#     updated_at = db.Column(db.DateTime,
#         default= db.func.now(),
#         onupdate=db.func.now())



# with app.app_context():
#         db.create_all()

@app.route("/services", methods=['POST' , 'GET', 'PATCH', 'DELETE'])
def services():
    if request.method == 'GET':
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

    if request.method == 'POST':

        body = request.get_json()

        new_service = Service(
            id = str(uuid.uuid4()),
            location = body['location'],
            services = body['service']
            )

        db.session.add(new_service)
        db.session.commit()

        return {'msg': 'Service created', 'id': new_service.id}

    if request.method == 'DELETE':      
        body = request.get_json()
        Service.query.filter_by(id = body['id']).delete()
    
        db.session.commit()

        return {'msg': 'Service deleted', 'id': body['id']}

    if request.method == 'PATCH': 
        body = request.get_json()
        
        service = Service.query.filter_by(id = body['id']).first()

        service.location = body['location'],
        service.services = body['service']

        db.session.commit()

        return {'msg': 'Service updated', 'location': body['location']}



# @app.route("/orders", methods=['POST', 'GET'])
# def orders():
#     if request.method == 'GET':
#         orders = []
#         for order in Order.query.all():
#             orders.append({
#                 'id:': order.id,
#                 'service_id': order.service_id,
#                 'location': order.location,
#                 'services': order.services,
#                 'created_at': order.created_at,
#                 'updated_at': order.updated_at
#             })

#     if request.method == 'POST':


#         body = request.get_json()

#         new_order = Order(
#             id = str(uuid.uuid4()),
#             location = body['location'],
#             services = body['service']
#             )

#         db.session.add(new_order)
#         db.session.commit()

#         return {'msg': 'Service created', 'id': new_order.id}

        



@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return { 
            'method': request.method,
            'msg': 'Github webhook deployment works!', 
            'env': os.environ.get('ENV_VAR', 'Cannot find variable ENV_VAR')
        }

    if request.method == 'POST':
        
        body = request.get_json()

        return {
            'msg': 'You POSTed something',
            'request_body': body
        }

@app.route("/users", methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        users = []
        for user in User.query.all():
            users.append({
            'id': user.id,
            'email': user.email,
            'created_at': user.created_at,
            'updated_at': user.updated_at
            })
        return users
    
    if request.method == 'POST':
        body = request.get_json()
        new_user = User(email = body['email'], id = str(uuid.uuid4()))
        db.session.add(new_user)
        db.session.commit()

        return {'msg': 'User created', 'id': new_user.id}


if __name__ == "__main__":
    app.run(debug=True, port=8080, host='0.0.0.0')
