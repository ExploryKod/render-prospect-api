import os
import argparse
from dotenv import load_dotenv
from app import create_app

load_dotenv()

def parse_arguments():
    parser = argparse.ArgumentParser(description='Prospects Flow Service')
    parser.add_argument('--port', '-p', type=int, 
                       default=int(os.getenv('FLASK_PORT', 5000)), 
                       help='Port to run the server on (default: 5000 or FLASK_PORT env var)')
    parser.add_argument('--host', type=str, 
                       default=os.getenv('FLASK_HOST', '0.0.0.0'),
                       help='Host to run the server on (default: 0.0.0.0 or FLASK_HOST env var)')
    parser.add_argument('--debug', action='store_true', 
                       default=os.getenv('FLASK_DEBUG', 'True').lower() == 'true',
                       help='Run in debug mode (default: True or FLASK_DEBUG env var)')
    return parser.parse_args()

app = create_app()

if __name__ == '__main__':
    args = parse_arguments()
    print(f"Starting Prospects Flow Service on {args.host}:{args.port}")
    print(f"Debug mode: {args.debug}")
    app.run(debug=args.debug, host=args.host, port=args.port) 