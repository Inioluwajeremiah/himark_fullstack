from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# db = SQLAlchemy(session_options={"autoflush": False})
db = SQLAlchemy()
DB_NAME = "hotel.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'd586404a06767db34f68e6531bc898eb'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # app.config['SQLALCHEMY_BINDS'] = {
    #     'admin_db': 'sqlite:///admin.db',
    #     'hotel_records': 'sqlite:///hotel_records.db'
    # }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import HotelModel, AdminModel

    with app.app_context():
        db.create_all()

    # create_database(app)

    loginManager = LoginManager()
    loginManager.login_view = 'auth.login'
    loginManager.init_app(app)

    @loginManager.user_loader
    def load_user(user_id):
        # (user_id)
        return models.AdminModel.query.get(int(user_id))

    return app


def create_database(app):
    if not path.exists('full_stack/' + DB_NAME):
        db.create_all(app=app)
        print('database created successfully')
