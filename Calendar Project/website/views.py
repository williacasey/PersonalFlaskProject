from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from . import db
import json
from .models import Snack, Ingredient, Day, Meal

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
    saved_snacks = Snack.query.all()
    saved_meals = Meal.query.all()
    return render_template("calendar.html", user=current_user, saved_snacks=saved_snacks, saved_meals=saved_meals)

@views.route('/day/<string:date>', methods=['GET'])
def day_view(date):
    date_obj = datetime.strptime(date, '%Y-%m-%d').date()

    next_day = (date_obj + timedelta(days=1)).strftime('%Y-%m-%d')
    prev_day = (date_obj - timedelta(days=1)).strftime('%Y-%m-%d')
    
    snacks_without_day = Snack.query.filter_by(day_id=None).all()
    
    day = Day.query.filter_by(date=date).first()
    if day is None:
        day = Day(date=date_obj)
        # Add any other initialization as needed
        db.session.add(day)
        db.session.commit()

    # Render a template, passing the Day object
    return render_template('day.html', user=current_user, day=day, next_day=next_day, prev_day=prev_day, snacks_without_day=snacks_without_day)

@views.route('/nutrition', methods=['GET', 'POST'])
@login_required
def nutrition():
    snacksNoDay = Snack.query.filter(Snack.day_id.is_(None)).all()
    snacksDay = Snack.query.filter(Snack.day_id.isnot(None)).all()
    ingredients = Ingredient.query.filter(Ingredient.meal_id.is_(None)).all()

    return render_template('nutrition.html', snacksNoDay=snacksNoDay, snacksDay=snacksDay, ingredients=ingredients, user=current_user)

@views.route('/create_snack', methods=['POST'])
@login_required
def create_snack():
    if request.method == 'POST':
        # Retrieve form data
        snack_name = request.form.get('snackName')
        calories = request.form.get('snackCalories')
        carbs = request.form.get('snackCarbs')
        protein = request.form.get('snackProteins')
        fat = request.form.get('snackFats')
        # Add additional fields as needed

        # Create a new Snack object
        new_snack = Snack(name=snack_name, calories=calories, carbs=carbs, protein=protein, fats=fat)
        # Set values for other fields

        # Add to the database
        db.session.add(new_snack)
        try:
            db.session.commit()
            flash('Snack created successfully!', 'success')
        except:
            db.session.rollback()
            flash('Error: Unable to create snack', 'error')

        return redirect(url_for('views.nutrition'))
    
@views.route('/create_snack_day', methods=['POST'])
@login_required
def create_snack_day():
    print('Create Snack Called')
    snack_name = request.form.get('snackName')
    calories = request.form.get('snackCalories')
    carbs = request.form.get('snackCarbs')
    protein = request.form.get('snackProteins')
    fats = request.form.get('snackFats')
    day_id = request.form.get('dayId')
    
    day = Day.query.filter_by(id=day_id).first()
    date = day.date
    
    # Check for existing snack with the same name
    existing_snack = Snack.query.filter_by(name=snack_name).first()
    if existing_snack:
        flash('Snack with this name already exists', 'error')
        return redirect(url_for('views.day_view', date=day_id))

    # Create new snack and associate it with the day
    new_snack = Snack(name=snack_name, calories=calories, carbs=carbs, protein=protein, fats=fats, day_id=day_id)
    db.session.add(new_snack)

    # Create a clone of the snack without a day_id
    clone_snack = Snack(name=snack_name, calories=calories, carbs=carbs, protein=protein, fats=fats)
    db.session.add(clone_snack)

    db.session.commit()
    flash('Snack created successfully', 'success')
    return redirect(url_for('views.day_view', date=date))

@views.route('/add_existing_snack', methods=['POST'])
@login_required
def add_existing_snack():
    snack_id = request.form.get('snackId')
    day_id = request.form.get('date')
    
    day = Day.query.filter_by(id=day_id).first()
    date = day.date
    
    snack = Snack.query.filter_by(id=snack_id).first()
    
    newSnack = Snack(name=snack.name, calories=snack.calories, carbs=snack.carbs, protein=snack.protein, fats=snack.fats, day_id=day.id)
    db.session.add(newSnack)
    db.session.commit()
    return redirect(url_for('views.day_view', date=date))

@views.route('/create_ingredient', methods=['POST'])
@login_required
def create_ingredient():
    if request.method == 'POST':
        # Retrieve form data
        ingredient_name = request.form.get('ingredientName')
        calories = request.form.get('ingredientCalories')
        carbs = request.form.get('ingredientCarbs')
        protein = request.form.get('ingredientProteins')
        fat = request.form.get('ingredientFats')

        # Add additional fields as needed

        # Create a new Ingredient object
        new_ingredient = Ingredient(name=ingredient_name, calories=calories, carbs=carbs, protein=protein, fats=fat)
        # Set values for other fields

        # Add to the database
        db.session.add(new_ingredient)
        try:
            db.session.commit()
            flash('Ingredient created successfully!', 'success')
        except:
            db.session.rollback()
            flash('Error: Unable to create ingredient', 'error')

        return redirect(url_for('views.nutrition'))
    
@views.route('/delete_snack/<int:snack_id>', methods=['POST'])
@login_required
def delete_snack(snack_id):
    snack = Snack.query.get(snack_id)
    if snack:
        db.session.delete(snack)
        try:
            db.session.commit()
            flash('Snack deleted successfully', 'success')
        except:
            db.session.rollback()
            flash('Error, unable to delete snack', 'error')
    else:
        flash('Snack not found', 'error')
    return redirect(url_for('views.nutrition'))

@views.route('/delete_snack_day/<int:snack_id>', methods=['POST'])
@login_required
def delete_snack_day(snack_id):
    snack = Snack.query.get(snack_id)
    day_id = snack.day_id
    day = Day.query.filter_by(id=day_id).first()
    if snack:
        db.session.delete(snack)
        try:
            db.session.commit()
            flash('Snack deleted successfully', 'success')
        except:
            db.session.rollback()
            flash('Error, unable to delete snack', 'error')
    else:
        flash('Snack not found', 'error')
    return redirect(url_for('views.day_view', date=day.date))