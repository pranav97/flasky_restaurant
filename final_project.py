

#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


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
session = DBSession()
app.secret_key = 'obvious key'


@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    session = DBSession()
    restaurants = session.query(Restaurant).all()
    return render_template("restaurants.html", restaurants=restaurants)


@app.route('/restaurant/new/',  methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        # return "POSTED up"
        newItem = Restaurant(name=request.form['name'])
        session = DBSession()  # create a new session
        session.add(newItem)
        session.commit()
        # print(newItem.name)
        return redirect((url_for('showRestaurants')))
    else:
        return render_template("newrestaurant.html")


@app.route('/restaurant/edit/<int:restaurant_id>/',  methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    session = DBSession()  # create a new session
    to_edit = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            to_edit.name = request.form['name']
        session.add(to_edit)
        session.commit()
        flash("{} menu item".format(to_edit.name))
        return redirect(url_for('showRestaurants'))
    else:
        return render_template(
            'editrestaurant.html', restaurant=to_edit)

    # return render_template("editrestaurant.html", restaurant=restaurant)

@app.route('/restaurant/delete/<int:restaurant_id>/',  methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    session = DBSession()
    edited = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == "POST":
        # return "posted up"
        if edited:
            session.delete(edited)
            session.commit()
            flash("Deleted menu item")
            return redirect(url_for('showRestaurants'))
    else:
        return render_template("deleterestaurant.html", restaurant=edited)

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
    # items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    # return render_template("menu.html", items=items, restaurant_id=restaurant_id, name=restaurant['name'])
    entre = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, course="Appetizer").all()
    mainc = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, course="Main Course").all()
    dess = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, course="Dessert").all()
    return render_template('menu.html', restaurant_id=restaurant_id, name=restaurant.name, entre=entre, main_course=mainc, desserts=dess)


@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form[
            'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session = DBSession() # create a new session
        session.add(newItem)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    session = DBSession()  # create a new session
    edited = session.query(MenuItem).filter_by(id=menu_id).one()
    # print(edited.name)
    if request.method == 'POST':
        if request.form['name']:
            edited.name = request.form['name']
            edited.description = request.form['description']
            edited.price = request.form['price']
            edited.course = request.form['course']
            edited.restaurant_id = restaurant_id
        session.add(edited)
        session.commit()
        flash("Edited menu item")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=edited)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    session = DBSession()
    edited = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == "POST":
        if edited:
            session.delete(edited)
            session.commit()
            flash("Deleted menu item")
            return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template("deletemenuitem.html", restaurant_id=restaurant_id, menu_id=menu_id, item=edited)


# api end points
@app.route('/restaurants/JSON')
def restaurantsJSON():
    session = DBSession()
    items = session.query(Restaurant).all()
    return jsonify(Restaurants=[i.serialize for i in items])


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



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
