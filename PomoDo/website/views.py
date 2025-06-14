from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        selected_image = request.form.get('profile_img')
        current_user.profile_img = selected_image
        db.session.commit()
        flash('Profile image updated', category='success')
        return redirect(url_for('views.home'))

    profile_images = ['default1.png', 'default2.png', 'default3.png']
    return render_template("home.html", user=current_user, images=profile_images)
