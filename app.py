from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=False)
    password = db.Column(db.String(144), unique=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password


class AdminSchema(ma.Schema):
    class Meta:
        fields = ('email', 'password')


admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)

# Endpoint to create a new guide


@app.route('/admin', methods=["POST"])
def add_admin():
    email = request.json['email']
    password = request.json['password']

    new_admin = Admin(email, password)

    db.session.add(new_admin)
    db.session.commit()

    admin = Admin.query.get(new_admin.id)

    return admin_schema.jsonify(admin)

# endpoint all admins


@app.route("/admins", methods=["GET"])
def get_admins():
    all_admins = Admin.query.all()
    result = admins_schema.dump(all_admins)
    return jsonify(result)


# endpoint single admin

@app.route("/admin/<id>", methods=["GET"])
def get_admin(id):
    admin = Admin.query.get(id)
    return admin_schema.jsonify(admin)

# Update edit admin


@app.route("/admin/<id>", methods=["PUT"])
def admin_update(id):
    admin = Admin.query.get(id)
    email = request.json['email']
    password = request.json['password']

    admin.email = email
    admin.password = password

    db.session.commit()
    return admin_schema.jsonify(admin)

# Endpoint delete Record


@app.route("/admin/<id>", methods=["DELETE"])
def admin_delete(id):
    admin = Admin.query.get(id)
    db.session.delete(admin)
    db.session.commit()

    return "admin was deleted"


if __name__ == '__main__':
    app.run(debug=True)
