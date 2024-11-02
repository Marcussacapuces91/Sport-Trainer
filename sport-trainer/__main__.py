import secrets

from flask import Flask, render_template, session, redirect, Response
from flask_bootstrap import Bootstrap5

from orm import User, db
from bp_user import UserBlueprint


class Application(Flask):

    DATABASE = 'sqlite:///sqlite.db'

    def __init__(self, import_name: str):
        super().__init__(import_name)
        Bootstrap5(self)
        self.config['SECRET_KEY'] = secrets.token_hex()
        self.config['SQLALCHEMY_DATABASE_URI'] = self.DATABASE
        self.config['SQLALCHEMY_ECHO'] = True
        db.init_app(self)

        # self.add_url_rule("/favicon.ico", redirect_to=self.url_for('static', filename='favicon.ico'))
        self.route("/")(self.index)
        self.register_blueprint(UserBlueprint(self.import_name, url_prefix='/user'))


    def init_db(self):
        with self.app_context():
            db.drop_all()
            db.create_all()
            with db.session.begin():
                user1 = User('marc@sibert.fr', 'Marcus 1', 'Marc SIBERT', 'password')
                user2 = User('test@sibert.fr', 'Marcus 2', 'Marc SIBERT', 'password')
                db.session.add_all((user1, user2))

            for user in db.session.scalars(db.select(User)):
                print(user)

    def index(self) -> Response|str:
        if 'user' not in session:
            return redirect("/user/login")
        else:
            stmt = db.select(User).where(User.id == session['user'])
            user = db.one_or_404(stmt, description="User not found!")
            if user.session_valid():
                return render_template('index.html', user=user)
            else:
                redirect("/user/login")


if __name__ == "__main__":
    app = Application(__name__)
    app.init_db()
    app.run(debug=True)
