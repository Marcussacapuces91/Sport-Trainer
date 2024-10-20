import secrets
import sqlite3
from sqlite3 import OperationalError

from flask import Flask, render_template, session, g
from flask_bootstrap import Bootstrap


class Application(Flask):

    DATABASE = 'sqlite.db'

    def __init__(self, import_name: str):
        super().__init__(import_name)
        Bootstrap(self)
        self.config['SECRET_KEY'] = secrets.token_hex()
        self.teardown_appcontext(self._close_connection)

        # self.add_url_rule("/", view_func=self.index)

    def _get_db(self):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(self.DATABASE)
        return db

    def init_db(self):
        with self.app_context():
            db = self._get_db()
            try:
                with self.open_resource('schema.sql', mode='r') as f:
                    db.executescript(f.read())
                db.commit()
            except OperationalError as e:
                print(f"SQL Error: {e} in 'schema.sql'")
                raise e

    def _close_connection(self, exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    @Flask.route("/")
    def index(self):
        session['user'] = 42
        print(session)
        db = self._get_db()
        row = db.execute(f"SELECT * FROM user WHERE id={session['user']}")
        print(row)
        return render_template('index.html')


if __name__ == "__main__":
    app = Application(__name__)
    app.init_db()
    app.run(debug=True)
