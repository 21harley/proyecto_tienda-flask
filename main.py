from flask import Flask
from flask import session  # Dict
from flask import request
from flask import redirect
from flask import render_template

from database import User
from database import Product

# blueprint

app = Flask(__name__)
app.secret_key = 'bootcamp_codigofacilito'


@app.route('/')
def index():
    _product = Product.all_product()
    return render_template('index.html', products=_product, user="false")

# GET = Obtener un recurso
# POST = Crear un recurso


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print(request.form)  # Dic

        _email = request.form.get('email')  # None
        _password = request.form.get('password')

        if _email and _password:
            user = User.create_user(_email, _password)  # INSERT
            session['user'] = user.id  # ID del usuario en la base de datos

            return redirect('/products')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form)  # Dic

        _email = request.form.get('email')  # None
        _password = request.form.get('password')

        if _email and _password:
            user = User.select().where((User.email == _email) and (
                User.password == ("cody_"+_password))).first()  # INSERT
            if (user != None):
                session['user'] = user.id
                return redirect('/products')
            else:
                return render_template("login.html", error="true")
            # return redirect('/products')

    return render_template('register.html')


@app.route('/products')
def products():
    user = User.get(session['user'])

    # _products = Product.select().where(Product.user == user) # 1
    _products = user.products

    return render_template('products/index.html', products=_products, total=len(_products))


@app.route('/products/create', methods=['GET', 'POST'])
def products_create():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')

        if name and price:
            # SELECT * FROM users WHERE id = <id>
            user = User.get(session['user'])

            # INSER INTO products(name, price, user_id) VALUES (name, price, user_id)
            Product.create(name=name, price=price, user=user)
            return redirect('/products')

    return render_template('products/create.html')


@app.route('/products/update/<id>', methods=['GET', 'POST'])
def products_update(id):

    _product = Product.select().where(Product.id == id).first()

    if request.method == 'POST':
        user = User.get(session['user'])
        if user.id == _product.user_id:
            _product.name = request.form.get('name')
            _product.price = request.form.get('price')
            _product.save()  # UPDATE products SET name=''
            return redirect('/products')

    return render_template('products/update.html', product=_product)


@app.route('/products/delete/<id>', methods=['GET', 'POST', 'DELETE'])
def products_delete(id):
    user = User.get(session['user'])
    _product = Product.select().where(Product.id == id).first()
    if user.id == _product.user_id:
        _product = Product.delete().where(Product.id == id)
        _product.execute()
    return redirect('/products')


@app.route('/logout', methods=['GET', 'POST'])
def seccion_logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
