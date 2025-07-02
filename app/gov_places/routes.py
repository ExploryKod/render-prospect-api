from app.gov_places import gov_places
from flask import request, jsonify
import requests
import os
import time
from datetime import datetime

# French Government Enterprise Search API
FRENCH_ENTERPRISE_API_BASE = "https://recherche-entreprises.api.gouv.fr"

# Mapping des types d'activités vers les codes NAF
ACTIVITY_TYPE_MAPPING = {
    # Restaurants et cafés
    'restaurant': ['56.10A', '56.10B', '56.10C', '56.10D', '56.10E', '56.10F'],
    'cafe': ['56.30A', '56.30B'],
    'boulangerie': ['47.24Z'],
    'patisserie': ['47.24Z'],
    
    # Services de santé
    'pharmacie': ['47.73Z'],
    'medecin': ['86.90A', '86.90B', '86.90C', '86.90D'],
    'dentiste': ['86.23Z'],
    'veterinaire': ['75.00Z'],
    
    # Services automobiles
    'garage': ['45.20A', '45.20B', '45.20C', '45.20D'],
    'station_service': ['47.30Z'],
    'carrosserie': ['45.20E'],
    
    # Services financiers
    'banque': ['64.11Z', '64.12Z', '64.19Z'],
    'assurance': ['65.11Z', '65.12Z', '65.20Z'],
    'poste': ['53.10Z'],
    
    # Commerce
    'supermarche': ['47.11Z'],
    'boutique': ['47.51Z', '47.52Z', '47.53Z', '47.54Z', '47.59Z'],
    'vetements': ['47.71Z'],
    'chaussures': ['47.72Z'],
    'informatique': ['47.41Z', '47.42Z', '47.43Z'],
    'telephonie': ['47.42Z'],
    'livres': ['47.61Z'],
    'jouets': ['47.65Z'],
    'sport': ['47.64Z'],
    
    # Services professionnels
    'avocat': ['69.10Z'],
    'comptable': ['69.20Z'],
    'consultant': ['70.21Z', '70.22Z', '70.29Z'],
    'architecte': ['71.11Z'],
    'notaire': ['69.10Z'],
    
    # Services aux particuliers
    'coiffeur': ['96.02Z'],
    'estheticien': ['96.09Z'],
    'pressing': ['96.01Z'],
    'photographe': ['74.20Z'],
    
    # Hôtellerie
    'hotel': ['55.10Z', '55.20Z'],
    'camping': ['55.30Z'],
    
    # Services publics
    'mairie': ['84.11Z', '84.12Z', '84.13Z'],
    'prefecture': ['84.11Z'],
    'gendarmerie': ['84.24Z'],
    'police': ['84.24Z'],
    
    # Éducation
    'ecole': ['85.10Z', '85.20Z', '85.31Z', '85.32Z'],
    'universite': ['85.42Z'],
    'formation': ['85.59Z'],
    
    # Loisirs et culture
    'cinema': ['59.14Z'],
    'theatre': ['90.01Z'],
    'musee': ['91.02Z'],
    'bibliotheque': ['91.01Z'],
    'salle_sport': ['93.11Z', '93.12Z', '93.13Z'],
    
    # Transport
    'taxi': ['49.32Z'],
    'location_voiture': ['77.11Z'],
    'gare': ['49.20Z'],
    'aeroport': ['51.21Z'],
    
    # Bâtiment et construction
    'plombier': ['43.22Z'],
    'electricien': ['43.21Z'],
    'peintre': ['43.30Z'],
    'menuisier': ['16.23Z'],
    'macon': ['43.99A'],
    
    # Industrie
    'imprimerie': ['18.11Z', '18.12Z', '18.13Z', '18.14Z'],
    'textile': ['13.10Z', '13.20Z', '13.30Z', '13.91Z', '13.92Z', '13.93Z', '13.94Z', '13.95Z', '13.96Z', '13.99Z'],
    'mecanique': ['25.50Z', '25.61Z', '25.62Z', '25.71Z', '25.72Z', '25.73Z', '25.99Z'],
    
    # Services informatiques
    'developpement_logiciel': ['62.01Z'],
    'conseil_informatique': ['62.02Z'],
    'hebergement_web': ['63.11Z'],
    'telecommunications': ['61.10Z', '61.20Z', '61.30Z', '61.90Z'],
    
    # Services de nettoyage
    'nettoyage': ['81.21Z', '81.22Z', '81.29Z'],
    'jardinage': ['81.30Z'],
    'securite': ['80.10Z', '80.20Z', '80.30Z'],
    
    # Services funéraires
    'pompes_funebres': ['96.03Z'],
    
    # Services divers
    'reparation': ['95.11Z', '95.12Z', '95.21Z', '95.22Z', '95.23Z', '95.24Z', '95.25Z', '95.29Z'],
    'location': ['77.11Z', '77.12Z', '77.21Z', '77.22Z', '77.29Z', '77.31Z', '77.32Z', '77.33Z', '77.34Z', '77.35Z', '77.39Z', '77.40Z'],
}

def get_naf_codes_for_type(activity_type):
    """
    Retourne les codes NAF correspondant à un type d'activité
    """
    return ACTIVITY_TYPE_MAPPING.get(activity_type.lower(), [])

def get_available_activity_types():
    """
    Retourne la liste des types d'activités disponibles
    """
    return list(ACTIVITY_TYPE_MAPPING.keys())

@gov_places.route('/places', methods=['GET'])
def get_gov_places():
    """Legacy endpoint - kept for compatibility"""
    pass

@gov_places.route('/enterprises/search', methods=['GET'])
def search_enterprises():
    """
    Search French enterprises using the government API
    Query parameters:
    - q: search query (company name, address, etc.)
    - code_postal: postal code filter
    - code_naf: NAF code filter (activity code)
    - effectif_min: minimum employee count
    - effectif_max: maximum employee count
    - entreprises_individuelles: true/false for individual enterprises
    """
    try:
        # Get query parameters
        query = request.args.get('q', '')
        code_postal = request.args.get('code_postal', '')
        code_naf = request.args.get('code_naf', '')
        effectif_min = request.args.get('effectif_min', '')
        effectif_max = request.args.get('effectif_max', '')
        entreprises_individuelles = request.args.get('entreprises_individuelles', '')
        
        if not query:
            return jsonify({
                'error': 'Query parameter "q" is required',
                'usage': 'Use ?q=company_name to search'
            }), 400
        
        # Build API URL
        api_url = f"{FRENCH_ENTERPRISE_API_BASE}/search"
        
        # Build query parameters
        params = {'q': query}
        
        if code_postal:
            params['code_postal'] = code_postal
        if code_naf:
            params['code_naf'] = code_naf
        if effectif_min:
            params['effectif_min'] = effectif_min
        if effectif_max:
            params['effectif_max'] = effectif_max
        if entreprises_individuelles:
            params['entreprises_individuelles'] = entreprises_individuelles
        
        # Make request to French government API
        headers = {
            'User-Agent': 'ProspectsFlowService/1.0',
            'Accept': 'application/json'
        }
        
        response = requests.get(api_url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Add metadata about the search
            result = {
                'query': query,
                'filters_applied': {k: v for k, v in params.items() if k != 'q'},
                'total_results': len(data.get('results', [])),
                'timestamp': datetime.now().isoformat(),
                'results': data.get('results', [])
            }
            
            return jsonify(result)
        
        else:
            return jsonify({
                'error': f'API request failed with status {response.status_code}',
                'details': response.text
            }), response.status_code
            
    except requests.exceptions.Timeout:
        return jsonify({
            'error': 'Request timeout - API may be overloaded',
            'note': 'French government API has a limit of 7 calls per second'
        }), 408
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': 'Network error',
            'details': str(e)
        }), 500
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500

@gov_places.route('/enterprises/search/geographic', methods=['GET'])
def search_enterprises_geographic_by_type():
    """
    Search enterprises by geographic location and activity type
    Query parameters:
    - lat: latitude (required)
    - lon: longitude (required)
    - radius: search radius in meters (default: 1000)
    - type: activity type (required) - see /activity-types for available types
    - effectif_min: minimum employee count (optional)
    - effectif_max: maximum employee count (optional)
    - entreprises_individuelles: true/false for individual enterprises (optional)
    """
    try:
        # Get query parameters
        lat = request.args.get('lat', '')
        lon = request.args.get('lon', '')
        radius = request.args.get('radius', '1000')
        activity_type = request.args.get('type', '')
        effectif_min = request.args.get('effectif_min', '')
        effectif_max = request.args.get('effectif_max', '')
        entreprises_individuelles = request.args.get('entreprises_individuelles', '')
        
        # Validate required parameters
        if not lat or not lon:
            return jsonify({
                'error': 'Both latitude (lat) and longitude (lon) parameters are required',
                'usage': 'Use ?lat=48.8566&lon=2.3522&type=restaurant&radius=1000'
            }), 400
        
        if not activity_type:
            return jsonify({
                'error': 'Activity type parameter "type" is required',
                'usage': 'Use ?lat=48.8566&lon=2.3522&type=restaurant&radius=1000',
                'available_types': get_available_activity_types()
            }), 400
        
        # Get NAF codes for the activity type
        naf_codes = get_naf_codes_for_type(activity_type)
        if not naf_codes:
            return jsonify({
                'error': f'Unknown activity type: {activity_type}',
                'available_types': get_available_activity_types()
            }), 400
        
        # Build API URL for geographic search
        api_url = f"{FRENCH_ENTERPRISE_API_BASE}/search"
        
        # Build query parameters
        params = {
            'lat': lat,
            'lon': lon,
            'radius': radius
        }
        
        # Add NAF codes to the search
        # Note: The French API might not support multiple NAF codes in one request
        # So we'll use the first one and filter results if needed
        if naf_codes:
            params['code_naf'] = naf_codes[0]
        
        if effectif_min:
            params['effectif_min'] = effectif_min
        if effectif_max:
            params['effectif_max'] = effectif_max
        if entreprises_individuelles:
            params['entreprises_individuelles'] = entreprises_individuelles
        
        headers = {
            'User-Agent': 'ProspectsFlowService/1.0',
            'Accept': 'application/json'
        }
        
        response = requests.get(api_url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            # Filter results by NAF codes if multiple codes are available
            if len(naf_codes) > 1:
                filtered_results = []
                for result in results:
                    result_naf = result.get('code_naf', '')
                    if result_naf in naf_codes:
                        filtered_results.append(result)
                results = filtered_results
            
            result = {
                'location': {'lat': lat, 'lon': lon, 'radius': radius},
                'activity_type': activity_type,
                'naf_codes_used': naf_codes,
                'filters_applied': {k: v for k, v in params.items() if k not in ['lat', 'lon', 'radius']},
                'total_results': len(results),
                'timestamp': datetime.now().isoformat(),
                'results': results
            }
            
            return jsonify(result)
        
        else:
            return jsonify({
                'error': f'API request failed with status {response.status_code}',
                'details': response.text
            }), response.status_code
            
    except requests.exceptions.Timeout:
        return jsonify({
            'error': 'Request timeout - API may be overloaded',
            'note': 'French government API has a limit of 7 calls per second'
        }), 408
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500

@gov_places.route('/activity-types', methods=['GET'])
def get_activity_types():
    """
    Get list of available activity types for geographic search
    """
    try:
        activity_types = get_available_activity_types()
        
        # Group activity types by category for better organization
        categories = {
            'restaurants_et_cafes': ['restaurant', 'cafe', 'boulangerie', 'patisserie'],
            'sante': ['pharmacie', 'medecin', 'dentiste', 'veterinaire'],
            'automobile': ['garage', 'station_service', 'carrosserie'],
            'finance': ['banque', 'assurance', 'poste'],
            'commerce': ['supermarche', 'boutique', 'vetements', 'chaussures', 'informatique', 'telephonie', 'livres', 'jouets', 'sport'],
            'services_professionnels': ['avocat', 'comptable', 'consultant', 'architecte', 'notaire'],
            'services_particuliers': ['coiffeur', 'estheticien', 'pressing', 'photographe'],
            'hotellerie': ['hotel', 'camping'],
            'services_publics': ['mairie', 'prefecture', 'gendarmerie', 'police'],
            'education': ['ecole', 'universite', 'formation'],
            'loisirs_culture': ['cinema', 'theatre', 'musee', 'bibliotheque', 'salle_sport'],
            'transport': ['taxi', 'location_voiture', 'gare', 'aeroport'],
            'batiment': ['plombier', 'electricien', 'peintre', 'menuisier', 'macon'],
            'industrie': ['imprimerie', 'textile', 'mecanique'],
            'informatique': ['developpement_logiciel', 'conseil_informatique', 'hebergement_web', 'telecommunications'],
            'services_nettoyage': ['nettoyage', 'jardinage', 'securite'],
            'services_divers': ['pompes_funebres', 'reparation', 'location']
        }
        
        return jsonify({
            'total_types': len(activity_types),
            'categories': categories,
            'all_types': activity_types,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500

@gov_places.route('/enterprises/<siren>', methods=['GET'])
def get_enterprise_by_siren(siren):
    """
    Get detailed information about a specific enterprise by SIREN number
    """
    try:
        if not siren or len(siren) != 9:
            return jsonify({
                'error': 'Invalid SIREN number',
                'note': 'SIREN must be exactly 9 digits'
            }), 400
        
        # Build API URL for specific enterprise
        api_url = f"{FRENCH_ENTERPRISE_API_BASE}/entreprises/{siren}"
        
        headers = {
            'User-Agent': 'ProspectsFlowService/1.0',
            'Accept': 'application/json'
        }
        
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return jsonify({
                'siren': siren,
                'timestamp': datetime.now().isoformat(),
                'enterprise': data
            })
        
        elif response.status_code == 404:
            return jsonify({
                'error': 'Enterprise not found',
                'siren': siren
            }), 404
        
        else:
            return jsonify({
                'error': f'API request failed with status {response.status_code}',
                'details': response.text
            }), response.status_code
            
    except requests.exceptions.Timeout:
        return jsonify({
            'error': 'Request timeout',
            'note': 'French government API has a limit of 7 calls per second'
        }), 408
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500

@gov_places.route('/enterprises/geographic', methods=['GET'])
def search_enterprises_geographic():
    """
    Search enterprises by geographic location
    Query parameters:
    - lat: latitude
    - lon: longitude
    - radius: search radius in meters (default: 1000)
    """
    try:
        lat = request.args.get('lat', '')
        lon = request.args.get('lon', '')
        radius = request.args.get('radius', '1000')
        
        if not lat or not lon:
            return jsonify({
                'error': 'Both latitude (lat) and longitude (lon) parameters are required',
                'usage': 'Use ?lat=48.8566&lon=2.3522&radius=1000'
            }), 400
        
        # Build API URL for geographic search
        api_url = f"{FRENCH_ENTERPRISE_API_BASE}/search"
        
        params = {
            'lat': lat,
            'lon': lon,
            'radius': radius
        }
        
        headers = {
            'User-Agent': 'ProspectsFlowService/1.0',
            'Accept': 'application/json'
        }
        
        response = requests.get(api_url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            result = {
                'location': {'lat': lat, 'lon': lon, 'radius': radius},
                'total_results': len(data.get('results', [])),
                'timestamp': datetime.now().isoformat(),
                'results': data.get('results', [])
            }
            
            return jsonify(result)
        
        else:
            return jsonify({
                'error': f'API request failed with status {response.status_code}',
                'details': response.text
            }), response.status_code
            
    except requests.exceptions.Timeout:
        return jsonify({
            'error': 'Request timeout',
            'note': 'French government API has a limit of 7 calls per second'
        }), 408
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500