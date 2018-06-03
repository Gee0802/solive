from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from solive import create_app, db


app = create_app()
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
migrate = Migrate(app, db, directory=app.config['SQLALCHEMY_MIGRATE_REPO'])
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
