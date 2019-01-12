from flask import Flask, \
    render_template, \
    request, redirect, \
    url_for, flash, \
    jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)


@app.route('/')
def defaultRestaurantMenu():
    session = DBSession()
    restaurant = session.query(Restaurant).first()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant_id=restaurant.id, name=restaurant.name, items=items)


@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    # Base.metadata.bind = engine
    #
    # DBSession = sessionmaker(bind=engine)
    session = DBSession()

    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return render_template('menu.html', restaurant_id=restaurant_id, name=restaurant.name, items=items)

@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    # Base.metadata.bind = engine
    #
    # DBSession = sessionmaker(bind=engine)
    # session = DBSession()
    session = DBSession()

    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    # Base.metadata.bind = engine
    #
    # DBSession = sessionmaker(bind=engine)
    session = DBSession()

    # print(menu_id)
    edited = session.query(MenuItem).filter_by(id=menu_id).one()
    # print(edited.name)
    if request.method == 'POST':
        if request.form['name']:
            edited.name = request.form['name']
        session.add(edited)
        session.commit()
        flash("Edited menu item")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
        # SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=edited)


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    # Base.metadata.bind = engine
    #
    # DBSession = sessionmaker(bind=engine)
    session = DBSession()

    edited = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == "POST":
        if edited:
            session.delete(edited)
            session.commit()
            flash("Deleted menu item")
            return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))

    else:
        return render_template("deletemenuitem.html",  restaurant_id=restaurant_id, menu_id=menu_id, item=edited)




@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    session = DBSession()

    # restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    session = DBSession()
    # items = session.query(Restaurant).filter_by(restaurant_id=restaurant_id).all()
    # return jsonify(MenuItem=items[menu_id].serialize())
    items = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(MenuItem=items.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
