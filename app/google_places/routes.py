from app.google_places import google_places, api, places_response
from flask import request, jsonify
from flask_restx import Resource
import requests
import os
import json

@api.route('/places')
class PlacesResource(Resource):
    @api.doc('get_places',
        params={
            'latitude': 'Latitude (requis)',
            'longitude': 'Longitude (requis)', 
            'type': 'Type de lieu (optionnel, défaut: restaurant)',
            'maxResults': 'Nombre maximum de résultats (optionnel, défaut: 20)',
            'radius': 'Rayon de recherche en mètres (optionnel, défaut: 1000.0)'
        },
        responses={
            200: ('Succès', places_response),
            400: 'Paramètres manquants ou invalides',
            500: 'Erreur serveur ou clé API manquante'
        }
    )
    def get(self):
        """
        Récupère les lieux dans une zone géographique via Google Places API
        
        Retourne uniquement le nom et l'adresse des lieux dans la zone spécifiée.
        """
        
        # Get query parameters
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
        place_type = request.args.get('type', 'restaurant')
        max_results = request.args.get('maxResults', 20, type=int)
        radius = request.args.get('radius', 1000.0, type=float)

        # Validate required parameters
        if not latitude or not longitude:
            api.abort(400, "latitude and longitude are required parameters")

        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            api.abort(400, "latitude and longitude must be valid numbers")

        # Get API key from environment variable
        api_key = os.getenv("GOOGLE_PLACE_API_KEY")
        if not api_key:
            api.abort(500, "Missing GOOGLE_API_KEY in environment")

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
            
            return {
                "success": True,
                "count": len(places),
                "places": places,
                "searchParams": {
                    "latitude": latitude,
                    "longitude": longitude,
                    "type": place_type,
                    "radius": radius
                }
            }
        else:
            api.abort(response.status_code, response.text)

@api.route('/mock-places')
class MockPlacesResource(Resource):
    @api.doc('get_mock_places',
        params={
            'latitude': 'Latitude (requis)',
            'longitude': 'Longitude (requis)', 
            'type': 'Type de lieu (optionnel, défaut: restaurant)',
            'maxResults': 'Nombre maximum de résultats (optionnel, défaut: 20)',
            'radius': 'Rayon de recherche en mètres (optionnel, défaut: 1000.0)'
        },
        responses={
            200: ('Succès', places_response),
            400: 'Paramètres manquants ou invalides',
            500: 'Erreur lors de la lecture du fichier mock'
        }
    )
    def get(self):
        """
        Récupère les données mock depuis le fichier mock_data.json
        
        Accepte les mêmes paramètres que l'API réelle pour la compatibilité frontend.
        """
        # Get query parameters (same as real API)
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
        place_type = request.args.get('type', 'restaurant')
        max_results = request.args.get('maxResults', 20, type=int)
        radius = request.args.get('radius', 1000.0, type=float)

        # Validate required parameters (same as real API)
        if not latitude or not longitude:
            api.abort(400, "latitude and longitude are required parameters")

        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            api.abort(400, "latitude and longitude must be valid numbers")

        try:
            # Get the path to the mock_data.json file - using the correct path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            mock_file_path = os.path.join(current_dir, 'mock_data.json')
            
            # Debug: print the path to help troubleshoot
            print(f"Looking for mock data at: {mock_file_path}")
            
            # Read the mock data
            with open(mock_file_path, 'r', encoding='utf-8') as file:
                mock_data = json.load(file)
            
            # Update the searchParams with the actual parameters sent by frontend
            mock_data['searchParams'] = {
                "latitude": latitude,
                "longitude": longitude,
                "type": place_type,
                "radius": radius
            }
            
            # Optionally limit results based on maxResults parameter
            if 'places' in mock_data and max_results < len(mock_data['places']):
                mock_data['places'] = mock_data['places'][:max_results]
                mock_data['count'] = len(mock_data['places'])
            
            return mock_data
            
        except FileNotFoundError:
            api.abort(500, f"Mock data file not found at: {mock_file_path}")
        except json.JSONDecodeError:
            api.abort(500, "Invalid JSON in mock data file")
        except Exception as e:
            api.abort(500, f"Error reading mock data: {str(e)}")