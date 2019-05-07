from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate

from dh_backend import create_app
from dh_backend.models import db

app = create_app()
app.migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
