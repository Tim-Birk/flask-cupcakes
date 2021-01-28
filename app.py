"""Flask app for Cupcakes"""
"""cupcake adoption application."""

from flask import Flask, render_template, flash, redirect, jsonify, request
from models import Cupcake, db, connect_db
# from forms import AddcupcakeForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route("/api/cupcakes")
def get_cupcakes():
    """List of cupcakes"""

    cupcakes = Cupcake.query.all()
    serialized = [cupcake.serialize() for cupcake in cupcakes]
    return jsonify(cupcakes=serialized)

@app.route("/api/cupcakes/<int:id>")
def get_cupcake(id):
    """Get single cupcake by id"""

    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())

@app.route("/api/cupcakes", methods=["POST"])
def add_cupcake():
    """Add new cupcake"""
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image'] if not request.json['image'] == "" else None

    flash(f"Added {flavor} cupcake!","success")

    cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(cupcake)
    db.session.commit()
    return (jsonify(cupcake=cupcake.serialize()), 201)

@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def edit_cupcake(id):
    """Show cupcake edit form and handle edit."""
    cupcake = Cupcake.query.get_or_404(id)

    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.commit()
    flash(f"Updated {cupcake.flavor}!","success")
    return (jsonify(cupcake=cupcake.serialize()), 200)

@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def delete_cupcake(id):
    """Delete cupcake from database"""

    cupcake = Cupcake.query.get_or_404(id)
    try:
        cupcake = cupcake.query.filter_by(id=id).first()
        db.session.delete(cupcake)
        db.session.commit()

        flash("Cupcake deleted", "success")
    except Exception as e:
        flash(f"There was an error deleting the cupcake: {e}", "error")
        return (jsonify(message="Error deleting cupcake"), 400)

    return (jsonify(message="Cupcake deleted!"), 200)