from flask import Blueprint, \
    render_template, \
    redirect, \
    url_for, \
    request, \
    flash, \
    jsonify
from .models import Restaurant, MenuItem
from flask_login import login_user, logout_user, login_required
from . import db

restaurants = Blueprint('restaurants', __name__)
@restaurants.route('/', methods=['GET'])
@restaurants.route('/restaurants/', methods=['GET'])
@login_required
def showRestaurants():
    # session = DBSession()
    restaurants = Restaurant.query.all()
    return render_template("restaurants.html", restaurants=restaurants)


@restaurants.route('/restaurant/new/',  methods=['GET', 'POST'])
@login_required
def newRestaurant():
    if request.method == 'POST':
        newItem = Restaurant(name=request.form['name'])
        db.session.add(newItem)
        db.session.commit()
        return redirect((url_for('restaurants.showRestaurants')))
    else:
        return render_template("newrestaurant.html")


@restaurants.route('/restaurant/edit/<int:restaurant_id>/',  methods=['GET', 'POST'])
@login_required
def editRestaurant(restaurant_id):
    to_edit = Restaurant.query().filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            to_edit.name = request.form['name']
        db.session.add(to_edit)
        db.session.commit()
        flash("{} menu item".format(to_edit.name))
        return redirect(url_for('restaurants.showRestaurants'))
    else:
        return render_template(
            'editrestaurant.html', restaurant=to_edit)

    # return render_template("editrestaurant.html", restaurant=restaurant)

@restaurants.route('/restaurant/delete/<int:restaurant_id>/',  methods=['GET', 'POST'])
@login_required
def deleteRestaurant(restaurant_id):
    toDelete = Restaurant.query.filter_by(id=restaurant_id).one()
    if request.method == "POST":
        if toDelete:
            db.session.delete(toDelete)
            relevant_menu_items = MenuItem.query.filter_by(restaurant_id=restaurant_id).all()
            for i in relevant_menu_items:
                db.session.delete(i)
            db.session.commit()
            flash("Deleted restaurant and related menu items")
            return redirect(url_for('restaurants.showRestaurants'))
    else:
        return render_template("deleterestaurant.html", restaurant=toDelete)


"""
# api end points
@app.route('/restaurants/JSON')
def restaurantsJSON():
    session = DBSession()
    items = session.query(Restaurant).all()
    return jsonify(Restaurants=[i.serialize for i in items])

"""