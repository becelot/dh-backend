import os

from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate

from dh_backend import create_migration_app
from dh_backend.models import db
from dh_backend.config import config

environment = os.environ.get('BUILD_MODE', 'dev')

app = create_migration_app(config=config[environment])
app.migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
