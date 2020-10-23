from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from src import create_app
from src.models import db

config_name = "development" # config_name = os.getenv('APP_SETTINGS') 
app = create_app(config_name)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
  manager.run()