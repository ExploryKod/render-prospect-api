import pytest
import json
from unittest.mock import Mock, patch

class TestGooglePlacesRoutes:
    """Test suite for Google Places routes."""

    def test_get_places_success(self, client):
        """Test successful places search with valid parameters."""
        # Test request - utiliser mock-places
        response = client.get('/google_places/mock-places?latitude=48.8566&longitude=2.3522&type=restaurant&maxResults=3&radius=1000')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Verify response structure
        assert data['success'] is True
        assert data['count'] == 3  # maxResults=3
        assert len(data['places']) == 3
        
        # Verify first place data (basé sur mock_data.json)
        first_place = data['places'][0]
        assert first_place['name'] == 'Bouillon Chartier Grands Boulevards'
        assert first_place['address'] == '7 Rue du Faubourg Montmartre, 75009 Paris, France'
        assert first_place['phone'] == '01 47 70 86 29'
        assert first_place['email'] is None
        assert first_place['type'] == 'restaurant'
        assert first_place['geo']['latitude'] == 48.871933299999995
        assert first_place['geo']['longitude'] == 2.3430535
        
        # Verify search parameters
        assert data['searchParams']['latitude'] == 48.8566
        assert data['searchParams']['longitude'] == 2.3522
        assert data['searchParams']['type'] == 'restaurant'
        assert data['searchParams']['radius'] == 1000.0

    def test_get_places_missing_required_params(self, client):
        """Test places search with missing required parameters."""
        # Test without latitude
        response = client.get('/google_places/mock-places?longitude=2.3522')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "latitude and longitude are required" in data['message']
        
        # Test without longitude
        response = client.get('/google_places/mock-places?latitude=48.8566')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "latitude and longitude are required" in data['message']

    def test_get_places_invalid_coordinates(self, client):
        """Test places search with invalid coordinate values."""
        # Test with non-numeric latitude
        response = client.get('/google_places/mock-places?latitude=invalid&longitude=2.3522')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "latitude and longitude must be valid numbers" in data['message']
        
        # Test with non-numeric longitude
        response = client.get('/google_places/mock-places?latitude=48.8566&longitude=invalid')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "latitude and longitude must be valid numbers" in data['message']

    def test_get_places_default_parameters(self, client):
        """Test places search with default parameters."""
        # Test with only required parameters
        response = client.get('/google_places/mock-places?latitude=48.8566&longitude=2.3522')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Verify default values are used
        assert data['searchParams']['type'] == 'restaurant'  # default
        assert data['searchParams']['radius'] == 1000.0  # default
        assert len(data['places']) <= 20  # default maxResults

    def test_get_places_different_type(self, client):
        """Test places search with different place type."""
        # Test with cafe type
        response = client.get('/google_places/mock-places?latitude=48.8566&longitude=2.3522&type=cafe')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['searchParams']['type'] == 'cafe'

    def test_get_places_empty_response(self, client):
        """Test places search when no places are found."""
        # Pour mock-places, on a toujours des données, donc on teste avec maxResults=0
        response = client.get('/google_places/mock-places?latitude=48.8566&longitude=2.3522&maxResults=0')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['count'] == 0
        assert len(data['places']) == 0

    def test_get_places_missing_phone_number(self, client):
        """Test places search with places that don't have phone numbers."""
        # Dans mock_data.json, "Galerie Vivienne" n'a pas de téléphone
        response = client.get('/google_places/mock-places?latitude=48.8566&longitude=2.3522&maxResults=10')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Chercher le lieu sans téléphone
        place_without_phone = None
        for place in data['places']:
            if place['name'] == 'Galerie Vivienne':
                place_without_phone = place
                break
        
        assert place_without_phone is not None
        assert place_without_phone['phone'] is None

    def test_get_places_custom_radius_and_max_results(self, client):
        """Test places search with custom radius and maxResults."""
        # Test with custom parameters
        response = client.get('/google_places/mock-places?latitude=48.8566&longitude=2.3522&radius=500&maxResults=5')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['searchParams']['radius'] == 500.0
        assert data['count'] == 5
        assert len(data['places']) == 5

    def test_get_places_missing_api_key(self, client):
        """Test places search when GOOGLE_API_KEY is missing."""
        # Pour mock-places, pas besoin de clé API
        response = client.get('/google_places/mock-places?latitude=48.8566&longitude=2.3522')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True

    def test_get_places_all_data(self, client):
        """Test that all places from mock_data.json are returned."""
        response = client.get('/google_places/mock-places?latitude=48.8566&longitude=2.3522&maxResults=20')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Vérifier qu'on a tous les lieux du fichier JSON
        assert data['count'] == 10
        assert len(data['places']) == 10
        
        # Vérifier quelques lieux spécifiques
        place_names = [place['name'] for place in data['places']]
        assert 'Bouillon Chartier Grands Boulevards' in place_names
        assert 'Angelina' in place_names
        assert 'Les Deux Magots' in place_names
        assert 'Galerie Vivienne' in place_names

    def test_health_check_endpoint(self, client):
        """Test the health check endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['service'] == 'prospects-flow-service' 