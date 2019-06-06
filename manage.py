import os
from datetime import datetime

from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate

from dh_backend import create_migration_app
from dh_backend.models import db, DeckVersion
from dh_backend.config import config
from dh_backend.models.Game import GameResult

environment = os.environ.get('BUILD_MODE', 'dev')

app = create_migration_app(config=config[environment])
app.migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def winloss():
    for version in db.session.query(DeckVersion).all():
        version.deck.win_count = 0
        version.deck.loss_count = 0
        version.win_count = 0
        version.loss_count = 0

        for game in version.games:
            if game.result == GameResult.RESULT_LOSS:
                version.loss_count += 1
                version.deck.loss_count += 1
            elif game.result == GameResult.RESULT_WIN:
                version.win_count += 1
                version.deck.win_count += 1

        version.last_played = datetime.now()

    db.session.commit()


if __name__ == '__main__':
    manager.run()
