from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/about')
def about():
    return render_template('aboutme.html') 

# @main.route('/profile')
# @login_required
# def profile():
#     return render_template('profile.html', name=current_user.name)
#
#todo add in the about page here
#todo add in the projects page here
