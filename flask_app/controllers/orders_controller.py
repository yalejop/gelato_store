from flask import render_template, redirect, session, request, flash

from flask_app import app

#importando el modelo de recetas
from flask_app.models.users import User
from flask_app.models.orders import Order
from flask_app.models.toppings import Topping 
from flask_app.models.types import Type
from flask_app.models.deliveries import Delivery
from flask_app.models.sizes import Size

@app.route('/new/order/')
def new_order():
    if 'user_id' not in session: #Solo puede ver la página si ya inició sesión 
        return redirect('/login/')

    formulario = {
        "id": session['user_id']
    }

    user = User.get_by_id(formulario)
    
    deliveries = Delivery.get_all_types()
    sizes = Size.get_all_sizes()
    toppings = Topping.get_all_toppings()
    types = Type.get_all_types()
    
    return render_template('new_ice_cream.html', user=user, toppings=toppings, types=types, deliveries=deliveries, sizes=sizes)

@app.route('/create/order/', methods=['POST'])
def create_recipe():
    if 'user_id' not in session: #Solo puede ver la página si ya inició sesión 
        return redirect('/login/')
    
    #Tengo que validar mi receta
    if not Order.validate_order(request.form): #Recipe.valida_receta(ENVIA FORMULARIO). SI NO ES VALIDO
        return redirect('/new/order/')

    Order.save(request.form)
    return redirect('/checkout/')

@app.route('/edit/recipe/<int:id>') #Recibo el identificador de la receta que quiero editar
def edit_recipe(id):
    if 'user_id' not in session: #Solo puede ver la página si ya inició sesión 
        return redirect('/')
    
    formulario = {
        "id": session['user_id']
    }

    user = User.get_by_id(formulario) #Usuario que inició sesión

    formulario_receta = { "id": id }
    #llamar a una función y debo de recibir la receta
    recipe = Order.get_by_id(formulario_receta)

    return render_template('edit_recipe.html', user=user, recipe=recipe)

@app.route('/update/recipe', methods=['POST'])
def update_order():
    if 'user_id' not in session: #Solo puede ver la página si ya inició sesión 
        return redirect('/')
    
    if not Order.valida_receta(request.form):
        return redirect('/edit/recipe/'+request.form['id']) #/edit/recipe/1

    Recipe.update(request.form)

    return redirect('/dashboard')

@app.route('/show/recipe/<int:id>') #A través de la URL recibimos el ID de la receta
def show_recipe(id):
    if 'user_id' not in session: #Solo puede ver la página si ya inició sesión 
        return redirect('/')

    formulario = {
        "id": session['user_id']
    }

    user = User.get_by_id(formulario) #Usuario que inició sesión


    formulario_receta = { "id": id }
    #llamar a una función y debo de recibir la receta
    recipe = Recipe.get_by_id(formulario_receta)

    return render_template('show_recipe.html', user=user, recipe=recipe)

@app.route('/delete/recipe/<int:id>')
def delete_recipe(id):
    if 'user_id' not in session: #Solo puede ver la página si ya inició sesión 
        return redirect('/')
    
    formulario = {"id": id}
    Recipe.delete(formulario)

    return redirect('/dashboard')

