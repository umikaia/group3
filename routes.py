from extensions import app, db
from flask import render_template, request, redirect, send_from_directory, flash
from forms import AddProduct, RegisterForm, LoginForm
from models import Product, Category, User
from flask_login import logout_user, login_user, login_required, current_user
import os

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/store")
def store():
    products = Product.query.all()
    return render_template("index.html", products=products)

@app.route("/addproduct", methods=["GET", "POST"])
def add_product():
    form = AddProduct()
    form.category.choices=[(category.id, category.name) for category in Category.query.all()]
    if form.validate_on_submit():
        file = request.files['file']
        if file: 
            filename = file.filename
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        kit = Product(name=form.name.data,
                      file=filename,
                      price=form.price.data,
                      category_id=form.category.data)
        db.session.add(kit)
        db.session.commit()
        return redirect("/store")
        
    return render_template("addproduct.html", form=form)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/detail/<int:id>')
def detail(id):
    current = Product.query.get(id)
    return render_template("details.html", product=current)
@app.route("/delete/<int:id>")
@login_required
def delete_product(id):
    if current_user.role == "admin":

        current = Product.query.get(id)
        print(current)
        db.session.delete(current)
        db.session.commit()
        return redirect("/store")
    else:
        return "You are not authorized, 404"


@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_product(id):
    if current_user.role == "admin":
        current = Product.query.get(id)
        form = AddProduct(name=current.name,
                        price=current.price,
                        category_id=current.category)
        form.category.choices=[(category.id, category.name) for category in Category.query.all()]
        if form.validate_on_submit():
            file = request.files['file']
            if file:
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            current.name = form.name.data
            current.file = filename
            current.price = form.price.data
            current.category_id = form.category.data
            db.session.commit()
            return redirect("/store")
    
        if form.errors:
            print(form.errors)
            for error in form.errors:
                 print(error)
        return render_template("addproduct.html", form=form)
    else:
        return "You are not authorized"

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect("/store")
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/store")
            
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route("/category/<int:category_id>")
def category_select(category_id):
    current_category = Category.query.get(category_id)
    products = Product.query.filter_by(category_id=category_id).all()
    return render_template("index.html", products=products)