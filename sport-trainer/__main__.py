import secrets

from flask import Flask, render_template, session, g, redirect, Response, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy


from orm import Base, User


class Application(Flask):

    DATABASE = 'sqlite:///sqlite.db'

    def __init__(self, import_name: str):
        super().__init__(import_name)
        Bootstrap5(self)
        self.config['SECRET_KEY'] = secrets.token_hex()
        self.config['SQLALCHEMY_DATABASE_URI'] = self.DATABASE
        # self.config['SQLALCHEMY_RECORD_QUERIES'] = True
        self.config['SQLALCHEMY_ECHO'] = True
        self.db = SQLAlchemy(model_class=Base)
        self.db.init_app(self)

        self.add_url_rule("/", view_func=self.index)
        self.add_url_rule("/login", view_func=self.login, methods=["GET","POST"])

    def init_db(self):
        with self.app_context():
            self.db.drop_all()
            self.db.create_all()
            with self.db.session.begin():
                user1 = User('marc@sibert.fr', 'Marcus 1', 'Marc SIBERT', 'password')
                user2 = User('test@sibert.fr', 'Marcus 2', 'Marc SIBERT', 'password')
                self.db.session.add_all((user1, user2))
            with self.db.session.execute(self.db.select(User)).scalars() as users:
                for user in users:
                    print(user)

    def index(self) -> Response|str:
        if 'user' not in session:
            return redirect("/login")

        print(session)
        db = self._get_db()
        try:
            user = User.get_from_id(db, session['user'])
        except TypeError as e:
            return "User not found!", 404
        return render_template('index.html', user=user)

    def login(self) -> str:
        if request.method == 'POST':
            print(request.form['email'], request.form['password'], request.form.get('remember'))
            stmt = self.db.select(User).filter_by(email=request.form['email'])
            user = self.db.session.execute(stmt).scalar_one()
            print(user.test_password(request.form['password']))
            return "POST"
        else:
            return render_template('login.html')


if __name__ == "__main__":
    app = Application(__name__)
    app.init_db()
    app.run(debug=True)
