from flask import Flask, jsonify, render_template
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Root route - render the main page
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Endpoint de santé pour Docker healthcheck
    @app.route('/health')
    def health_check():
        return jsonify({'status': 'healthy', 'service': 'prospects-flow-service'}), 200
        
    from app.google_places import google_places
    app.register_blueprint(google_places, url_prefix='/google_places')
    
    # Register LLM blueprint
    from app.llm import llm
    app.register_blueprint(llm, url_prefix='/llm')
    
    return app 