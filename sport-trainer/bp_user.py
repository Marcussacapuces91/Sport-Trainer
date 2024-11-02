from flask import Blueprint, session, redirect, Response, request, render_template, url_for
from sqlalchemy.exc import NoResultFound

from orm import User, db


class UserBlueprint(Blueprint):
    def __init__(self, import_name, **kwargs):
        super().__init__('UserBlueprint', import_name, **kwargs)

        self.route('/login', methods=['GET', 'POST'])(self.login)
        self.route('/profil')(self.profile)
        self.route('/disconnect')(self.disconnect)

    def login(self) -> Response|str:
        if request.method == 'POST':
            stmt = db.select(User).where(User.email == request.form['email'])
            try:
                with db.session.begin():
                    user = db.session.execute(stmt).scalar_one()
                    if user.test_password(request.form['password']):
                        user.set_session()
                        session['user'] = user.id
                        return redirect("/")
            except NoResultFound as e:
                pass

            print("Compte invalide!")
            return render_template('user/login.html')

        elif request.method == 'GET':
            return render_template('user/login.html')
        else:
            return Response("Error 404", 404)

    def profile(self):
        user = db.session.get_one(User, session['user'])
        return render_template('user/profile.html', user=user)

    def disconnect(self):
        session.clear()
        return redirect('/')