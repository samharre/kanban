import os
from src import create_app
 
app = create_app(os.getenv('APP_SETTINGS'))

if __name__ == '__main__':
    app.run()