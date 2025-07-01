import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # SQLITE FOR TESTS
    # SECRET_KEY = os.environ.get('SECRET KEY')
    # app.config['SQLALCHEMY_DATABASE_URI'] =\
    #         'sqlite:///' + os.path.join(basedir, 'game.db')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
    #     or 'sqlite:///' + os.path.join(basedir, 'game.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Creating an SQLAlchemy instance
    # db = SQLAlchemy(app)

    # API 
    GOOGLE_PLACE_API_KEY = os.environ.get('GOOGLE_PLACE_API_KEY')
    
    # Configuration pour Gunicorn
    WORKERS = 4
    BIND_ADDRESS = '0.0.0.0:5000'
    TIMEOUT = 60

    # Configuration pour Ollama
    if os.environ.get('ENV') == 'dev':
        OLLAMA_URL =  "https://88.222.221.12:11434/api/generate"
    else:
        OLLAMA_URL =  "http://127.0.0.1:11434/api/generate"