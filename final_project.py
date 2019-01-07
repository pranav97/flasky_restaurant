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
def allRestaurants():
    return "This is all the restaurants"


@app.route('/restaurants/create')
def createRestaurant():
    return "Create a restaurant page"


@app.route('/restaurants/edit/<int:restaurant_id>/')
def editRestaurant(restaurant_id):
    return "Edit a restaurant {}".format(restaurant_id)


@app.route('/restaurants/delete/<int:restaurant_id>/')
def deleteRestaurant(restaurant_id):
    return "Delete a restaurant {}".format(restaurant_id)


@app.route('/restaurants/new/')
def newRestaurant():
    return "Create a new restaurant"



if __name__ == '__main__':
    # app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
