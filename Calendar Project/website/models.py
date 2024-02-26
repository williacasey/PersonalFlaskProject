from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

class Day(db.Model):
    __tablename__ = 'days'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, unique=True)
    snacks = db.relationship('Snack', backref='day', lazy=True)
    meals = db.relationship('Meal', backref='day', lazy=True)

    def __init__(self, date):
        self.date = date

    def add_snack(self, snack):
        if not self.snacks:
            self.snacks = []
        self.snacks.append(snack)
        db.session.commit()

    def add_meal(self, meal):
        if not self.meals:
            self.meals = []
        self.meals.append(meal)
        db.session.commit()

class Snack(db.Model):
    __tablename__ = 'snacks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    carbs = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Integer, nullable=False)
    fats = db.Column(db.Integer, nullable=False)
    day_id = db.Column(db.Integer, db.ForeignKey('days.id'), nullable=True)
    
    def __init__(self, name, calories, carbs, protein, fats, day_id=None):
        self.name = name
        self.calories = calories
        self.carbs = carbs
        self.protein = protein
        self.fats = fats
        self.day_id = day_id

class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    carbs = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Integer, nullable=False)
    fats = db.Column(db.Integer, nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=True)
    
    def __init__(self, name, calories, carbs, protein, fats, meal_id=None):
        self.name = name
        self.calories = calories
        self.carbs = carbs
        self.protein = protein
        self.fats = fats
        self.meal_id = meal_id

class Meal(db.Model):
    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    day_id = db.Column(db.Integer, db.ForeignKey('days.id'), nullable=True)
    
    ingredients = db.relationship('Ingredient', backref='meal', lazy=True)

    def __init__(self, name, day_id=None, ingredients=None):
        self.name = name
        self.day_id = day_id

        if ingredients is None:
            ingredients = []

        for ingredient in ingredients:
            self.add_ingredient(ingredient)

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def save_to_database(self):
        db.session.add(self)
        db.session.commit()

        # Save associated ingredients
        for ingredient in self.ingredients:
            ingredient.meal_id = self.id
            db.session.add(ingredient)

        db.session.commit()