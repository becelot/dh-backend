import os

from dh_backend import create_app
from dh_backend.config import config

environment = os.environ.get('BUILD_MODE', 'dev')
application = create_app(config=config[environment])

if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0', port=5000)
