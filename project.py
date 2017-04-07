from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)

@app.route('/')
@app.route('/restaurants')
def list_restaurants():
    session = DBSession()
    restaurants = session.query(Restaurant).all()
    output = ""
    for restaurant in restaurants:
        output += "<h2>(%s). %s</h2><ol>" % (restaurant.id, restaurant.name)
        items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
        for item in items:
            output += "<li><ul><li><b>Name:</b> %s</li>" % (item.name)
            output += "<li><b>Price:</b> %s</li>" % (item.price)
            output += "<li><b>Description:</b> %s</li></ul></li>" % (item.description)
        output += "</ol><br>"
    session.close()
    return output

@app.route('/restaurant/<int:restaurant_id>/')
def list_restaurant(restaurant_id):
    session = DBSession()
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    session.close()
    return render_template("menu.html", restaurant=restaurant, items=items)

@app.route('/restaurant/<int:restaurant_id>/JSON')
def list_restaurantJson(restaurant_id):
    session = DBSession()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    session.close()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/JSON')
def menuItemJson(restaurant_id, menu_id):
    session = DBSession()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id)
    session.close()
    return jsonify(MenuItems=[i.serialize for i in items])


# Task 1: Create route for newMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == "POST":
        session = DBSession()
        newItem = MenuItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], restaurant_id= restaurant_id)
        session.add(newItem)
        session.commit()
        session.close()
        flash("Item inserted")
        return redirect(url_for('list_restaurant', restaurant_id = restaurant_id))
    else:
        session = DBSession()
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
        session.close()
        return render_template("newmenuitem.html", restaurant=restaurant)


# Task 2: Create route for editMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == "POST":
        session = DBSession()
        menuitem = session.query(MenuItem).filter_by(id=menu_id, restaurant_id=restaurant_id).first()
        menuitem.name = request.form['name']
        menuitem.description = request.form['description']
        menuitem.price = request.form['price']
        session.add(menuitem)
        session.commit()
        session.close()
        flash("Item edited")
        return redirect(url_for('list_restaurant', restaurant_id = restaurant_id))
    else:
        session = DBSession()
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
        menuitem = session.query(MenuItem).filter_by(id=menu_id, restaurant_id=restaurant_id).first()
        session.close()
        return render_template("editmenuitem.html", restaurant=restaurant, item=menuitem)

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    session = DBSession()
    menuitem = session.query(MenuItem).filter_by(id=menu_id, restaurant_id=restaurant_id).first()
    if request.method == "POST":
        session.delete(menuitem)
        session.commit()
        session.close()
        flash("Item deleted")
        return redirect(url_for('list_restaurant', restaurant_id = restaurant_id))
    else:
        session.close()
        return render_template("deletemenuitem.html", restaurant_id = restaurant_id, menu_id = menu_id, item = menuitem)


if __name__ == '__main__':
    app.secret_key = 'super_secrect_key'
    app.debug = True
    app.run(host = "0.0.0.0", port = 5000)