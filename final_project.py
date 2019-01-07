from flask import Flask, \
    render_template, \
    request, redirect, \
    url_for, flash, \
    jsonify
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)


@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    return "This is all the restaurants"


@app.route('/restaurant/new/')
def newRestaurant():
    return "Create a new restaurant"


@app.route('/restaurant/edit/<int:restaurant_id>/')
def editRestaurant(restaurant_id):
    return "Edit a restaurant {}".format(restaurant_id)


@app.route('/restaurant/delete/<int:restaurant_id>/')
def deleteRestaurant(restaurant_id):
    return "Delete a restaurant {}".format(restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    return "showing restaurant menu {}".format(restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
    return "New manu item for restaurant {}".format(restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    return "edit manu item for restaurant {}, menu_id {}".format(restaurant_id, menu_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return "delete manu item for restaurant {}, menu item {}".format(restaurant_id, menu_id)


if __name__ == '__main__':
    # app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
