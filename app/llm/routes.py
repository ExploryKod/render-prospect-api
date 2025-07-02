from app.llm import llm
from flask import request, jsonify
import requests
import os
from config import Config
@llm.route('/generate', methods=['POST'])
def call_ollama():
    """
    Route POST /llm/generate
    Call Ollama API to generate text based on a prompt
    
    JSON payload:
      - prompt (required): The text prompt to send to the LLM
      - model (optional): The model to use (default: 'mistral:latest')
      - stream (optional): Whether to stream the response (default: False)
    """
    
    # Get JSON data from request
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    
    data = request.get_json()
    
    # Validate required parameters
    if not data or 'prompt' not in data:
        return jsonify({"error": "prompt is required in the JSON payload"}), 400
    
    prompt = data.get('prompt')
    model = data.get('model', 'mistral:latest')
    stream = data.get('stream', False)
    
    if not prompt or not isinstance(prompt, str):
        return jsonify({"error": "prompt must be a non-empty string"}), 400
    
    # Debug information
    print(f"ENV variable: {os.environ.get('ENV', 'not set')}")
    print(f"Using Ollama URL: {Config.OLLAMA_URL}")
    
    # Prepare payload for Ollama API
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream
    }
    
    try:
        # Call Ollama API
        print(f"Sending request to: {Config.OLLAMA_URL}")
        print(f"Payload: {payload}")
        
        response = requests.post(Config.OLLAMA_URL, json=payload, timeout=120)
        
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {response.headers}")
        
        if response.status_code == 200:
            response_data = response.json()
            return jsonify({
                "success": True,
                "response": response_data.get("response", ""),
                "model": model,
                "done": response_data.get("done", True)
            })
        else:
            print(f"Error response: {response.text}")
            return jsonify({
                "success": False,
                "error": f"Ollama API error: {response.text}",
                "status_code": response.status_code
            }), response.status_code
            
    except requests.exceptions.Timeout:
        return jsonify({
            "success": False,
            "error": "Request to Ollama API timed out"
        }), 504
        
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
        return jsonify({
            "success": False,
            "error": "Could not connect to Ollama API. Make sure Ollama is running."
        }), 503
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }), 500

@llm.route('/models', methods=['GET'])
def list_models():
    """
    Route GET /llm/models
    List available models from Ollama
    """
    
    try:
        # Call Ollama API to list models
        response = requests.get(Config.OLLAMA_URL + "/api/tags", timeout=30)
        
        if response.status_code == 200:
            return jsonify({
                "success": True,
                "models": response.json()
            })
        else:
            return jsonify({
                "success": False,
                "error": f"Ollama API error: {response.text}",
                "status_code": response.status_code
            }), response.status_code
            
    except requests.exceptions.ConnectionError:
        return jsonify({
            "success": False,
            "error": "Could not connect to Ollama API. Make sure Ollama is running."
        }), 503
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }), 500

@llm.route('/health', methods=['GET'])
def health_check():
    """
    Route GET /llm/health
    Check if Ollama API is accessible
    """
    
    try:
        response = requests.get(Config.OLLAMA_URL + "/api/tags", timeout=10)
        
        if response.status_code == 200:
            return jsonify({
                "success": True,
                "status": "Ollama API is accessible",
                "url": Config.OLLAMA_URL
            })
        else:
            return jsonify({
                "success": False,
                "status": "Ollama API returned an error",
                "status_code": response.status_code
            }), 503
            
    except requests.exceptions.ConnectionError:
        return jsonify({
            "success": False,
            "status": "Could not connect to Ollama API",
            "url": Config.OLLAMA_URL
        }), 503
        
    except Exception as e:
        return jsonify({
            "success": False,
            "status": f"Unexpected error: {str(e)}"
        }), 500 