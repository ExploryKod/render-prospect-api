from app.google_places import google_places
from flask import request, jsonify
import requests
import os

@google_places.route('/places', methods=['GET'])
def get_places():
    """
    Route GET /google_places/places
    Returns only name and address of places in a zone
    
    Query parameters:
      - latitude (required)
      - longitude (required)
      - type (optional, default: 'restaurant')
      - maxResults (optional, default: 20)
      - radius (optional, default: 1000.0)
    """
    
    # Get query parameters
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    place_type = request.args.get('type', 'restaurant')
    max_results = request.args.get('maxResults', 20, type=int)
    radius = request.args.get('radius', 1000.0, type=float)

    # Validate required parameters
    if not latitude or not longitude:
        return jsonify({"error": "latitude and longitude are required parameters"}), 400

    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        return jsonify({"error": "latitude and longitude must be valid numbers"}), 400

    # Get API key from environment variable
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return jsonify({"error": "Missing GOOGLE_API_KEY in environment"}), 500

    url = "https://places.googleapis.com/v1/places:searchNearby"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location,places.nationalPhoneNumber,places.internationalPhoneNumber,places.types"
    }

    payload = {
        "includedTypes": [place_type],
        "maxResultCount": max_results,
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "radius": radius
            }
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        
        # Transform to format with name, address, phone, email, type, and geo
        places = []
        if 'places' in data:
            for place in data['places']:
                place_data = {
                    "name": place.get('displayName', {}).get('text', 'Unknown Place'),
                    "address": place.get('formattedAddress', 'No address available'),
                    "phone": place.get('nationalPhoneNumber') or place.get('internationalPhoneNumber'),
                    "email": None,  # Google Places API doesn't provide email addresses
                    "type": place_type,
                    "geo": {
                        "latitude": place.get('location', {}).get('latitude'),
                        "longitude": place.get('location', {}).get('longitude')
                    }
                }
                places.append(place_data)
        
        return jsonify({
            "success": True,
            "count": len(places),
            "places": places,
            "searchParams": {
                "latitude": latitude,
                "longitude": longitude,
                "type": place_type,
                "radius": radius
            }
        })
    else:
        return jsonify({
            "success": False,
            "error": response.text,
            "status_code": response.status_code
        }), response.status_code