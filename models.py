from extensions import app, db
from flask_login import UserMixin
from extensions import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
class Product(db.Model):
    name = db.Column(db.String)
    file = db.Column(db.String)
    price = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    product_id = db.relationship('Product', backref='category', lazy=True)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, default='guest')

    def __init__(self, username, password, role='guest'):
        self.username = username
        self.role = role
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        new_season = Category(name='New Season')
        special_edition = Category(name='Special Edition')
        retro = Category(name='Retro')
        national_team = Category(name="National Team")
 
        user = User(username="Ucha", password="webuser")
        admin = User(username="UchaAdmin", password="webadmin", role="admin")

        db.session.add_all([new_season, special_edition, retro, national_team, user, admin])
        db.session.commit()

        

