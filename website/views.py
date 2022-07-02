
from flask import Blueprint, Flask, render_template, request, session, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, EmailField
from wtforms.validators import DataRequired
from .models import recipes_collection
import re

views = Blueprint('views', __name__)

# @views.route('/')
# def base():
#     return render_template('base.html')

# classe form search

class FormSearch(FlaskForm):
    numIngredients = SelectField(u"Quanti ingredienti hai? ", choices=[("1", "1"), ("2", "2"), ("3", "3")])
    ingredientOne = StringField("Ingrediente 1: ", [DataRequired()])
    ingredientTwo = StringField("Ingrediente 2: ")
    ingredientThree = StringField("Ingrediente 3: ")
    submit = SubmitField("Cerca")

@views.route('/Search', methods=['GET','POST'])
def search():
    ing1 = ""
    ing2 = ""
    ing3 = ""
    prevUrl = request.referrer

    form=FormSearch()
    if form.validate_on_submit():
        ing1 = form.ingredientOne.data
        ing2 = form.ingredientTwo.data
        ing3 = form.ingredientThree.data
        if ing2 == "":
            ing2 = " "
        if ing3 == "":
            ing3 = " "
        
        form.numIngredients.data = ""
        form.ingredientOne.data = ""
        form.ingredientTwo.data = ""
        form.ingredientThree.data = ""

        return redirect(url_for('views.search_results', ing1=ing1, ing2=ing2, ing3=ing3))
    
    form.numIngredients.data = ""
    form.ingredientOne.data = ""
    form.ingredientTwo.data = ""
    form.ingredientThree.data = ""
    
    return render_template('search.html', form=form, prevUrl=prevUrl)


@views.route('/Risultati_ricerca/<ing1>/<ing2>/<ing3>')
def search_results(ing1, ing2, ing3):
    ingredients = f" {ing1}"
    if ing2 != " ":
        ingredients += f", {ing2}"
    if ing3 != " ":
        ingredients += f", {ing3}"

    recipes = list(recipes_collection.find({"ingredients": {"$regex": ing1}},{"_id": 0}))
    middleRes1 = recipes
    middleRes2 = []
    middleRes3 = []
    if ing2 != " ":
        for recipe in recipes:
            res2 = re.search(rf".*({ing2}).*", recipe['ingredients'])
            if res2 != None:
                middleRes2.append(recipe)
        if len(middleRes2) > 0:
            recipes = middleRes2
        if ing3 != " ":
            for recipe in recipes:
                res3 = re.search(rf".*({ing3}).*", recipe['ingredients'])
                if res3 != None:
                    middleRes3.append(recipe)
        if len(middleRes3) > 0:
            recipes = middleRes3
    
    if len(recipes) == 0:
        flash("Nessuna ricetta trovata", "error")
        return redirect(url_for('views.search'))
    elif len(recipes) == 1:
        nameRecipe = recipes[0]['name']
        return redirect(url_for('views.single_recipe', name=nameRecipe))

    return render_template('search_results.html', ingredients=ingredients, recipes=recipes, middleRes2=middleRes2, middleRes1=middleRes1)

@views.route('/Ricetta/<name>')
def single_recipe(name):
    recipe = dict(recipes_collection.find_one({"name": name},{"_id": 0}))
    return render_template('single_recipe.html', recipe=recipe.values())

@views.route('/')
def home():
    return render_template('homepage.html')