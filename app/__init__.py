from flask import Flask, jsonify, render_template
from config import Config
from flask_cors import CORS

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    #  # Enable CORS for all routes
    # CORS(app, resources={
    #     r"/*": {
    #         "origins": [
    #             "http://localhost:5173",  # Your React dev server
    #             "http://localhost:3000",  # Alternative React port
    #             "http://127.0.0.1:5173",
    #             "http://127.0.0.1:3000",
    #             "*",
    #             "http://127.0.0.1:8080",
    #             # Add your production frontend URL here when deployed
    #             # "https://your-frontend-domain.com"
    #         ],
    #         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    #         "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"]
    #     }
    # })
    
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Root route - Homepage
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # API Documentation route
    @app.route('/api-gov-docs')
    def api_gov_docs():
        return render_template('api_gov_docs.html')
    
    # API Documentation route
    @app.route('/api-google-docs')
    def api_google_docs():
        return render_template('google_docs.html')
    
    # Endpoint de santé pour Docker healthcheck
    @app.route('/health')
    def health_check():
        return jsonify({'status': 'healthy', 'service': 'prospects-flow-service'}), 200
        
    from app.google_places import google_places
    app.register_blueprint(google_places, url_prefix='/google_places')
    
    # Register LLM blueprint
    from app.llm import llm
    app.register_blueprint(llm, url_prefix='/llm')
    
    # Register French Government API blueprint
    from app.gov_places import gov_places
    app.register_blueprint(gov_places, url_prefix='/gov_places')
    
    return app 