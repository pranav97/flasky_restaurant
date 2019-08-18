from flask import Blueprint, \
    render_template, \
    redirect, \
    url_for, \
    request, \
    flash, \
    jsonify
from .models import Restaurant, MenuItem
from flask_login import login_user, logout_user, login_required, current_user
from . import db

menu = Blueprint('menu', __name__)

@login_required
@menu.route('/restaurant/<int:restaurant_id>/')
@menu.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    restaurant = Restaurant.query.filter_by(id=restaurant_id).first()
    soups = MenuItem.query.filter_by(restaurant_id=restaurant_id, course="Soup").all()
    appetizer = MenuItem.query.filter_by(restaurant_id=restaurant_id, course="Appetizer").all()
    mainc = MenuItem.query.filter_by(restaurant_id=restaurant_id, course="Main Course").all()
    sides = MenuItem.query.filter_by(restaurant_id=restaurant_id, course="Side Order").all()
    dess = MenuItem.query.filter_by(restaurant_id=restaurant_id, course="Dessert").all()
    beverages = MenuItem.query.filter_by(restaurant_id=restaurant_id, course="Beverage").all()
    return render_template('menu.html', 
        restaurant_id=restaurant_id, 
        name=restaurant.name, 
        appetizer=appetizer, 
        soups=soups, 
        sides=sides,
        main_course=mainc, 
        desserts=dess,
        beverages=beverages)

@login_required
@menu.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form[
            'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        db.session.add(newItem)
        db.session.commit()
        return redirect(url_for('menu.showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

@login_required
@menu.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    edited = MenuItem.query.filter_by(id=menu_id).one()
    to_edit = Restaurant.query.filter_by(id=restaurant_id).one()

    if edited is None:
        flash("Sorry, that is not a valid menu item.")
        return redirect(url_for('menu.showMenu', restaurant_id=restaurant_id))

    if current_user.id != to_edit.user_id:
        flash("Sorry, you don't have permissions to edit {}. Please edit something you created. ".format(to_edit.name))
        return redirect(url_for('menu.showMenu', restaurant_id=restaurant_id))

    if request.method == 'POST':
        if request.form['name']:
            edited.name = request.form['name']
            edited.description = request.form['description']
            edited.price = request.form['price']
            edited.course = request.form['course']
            edited.restaurant_id = restaurant_id
        db.session.add(edited)
        db.session.commit()
        flash("Edited menu item")
        return redirect(url_for('menu.showMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=edited)


@login_required
@menu.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    edited = MenuItem.query.filter_by(id=menu_id).one()
    toDelete = Restaurant.query.filter_by(id=restaurant_id).one()

    if edited is None:
        flash("Sorry, that is not a valid menu item.")
        return redirect(url_for('menu.showMenu', restaurant_id=restaurant_id))

    if current_user.id != toDelete.user_id:
        flash("Sorry, you don't have permissions to edit {}. Please edit something you created. ".format(toDelete.name))
        return redirect(url_for('menu.showMenu', restaurant_id=restaurant_id))

    if request.method == "POST":
        if edited:
            db.session.delete(edited)
            db.session.commit()
            flash("Deleted menu item")
            return redirect(url_for('menu.showMenu', restaurant_id=restaurant_id))
    else:
        return render_template("deletemenuitem.html", restaurant_id=restaurant_id, menu_id=menu_id, item=edited)

"""
# api end points
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    session = DBSession()

    # restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    session = DBSession()
    # items = session.query(Restaurant).filter_by(restaurant_id=restaurant_id).all()
    # return jsonify(MenuItem=items[menu_id].serialize())
    items = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(MenuItem=items.serialize)

"""
