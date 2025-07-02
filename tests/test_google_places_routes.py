import pytest
import json
from unittest.mock import Mock, patch
from app.google_places.routes import get_places

class TestGooglePlacesRoutes:
    """Test suite for Google Places routes."""

    def test_get_places_success(self, client, mock_requests_post, mock_google_places_response):
        """Test successful places search with valid parameters."""
        # Mock the successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_google_places_response
        mock_requests_post.return_value = mock_response

        # Test request
        with patch.dict('os.environ', {'GOOGLE_API_KEY': 'fake-api-key'}):
            response = client.get('/google_places/places?latitude=48.8566&longitude=2.3522&type=restaurant&maxResults=3&radius=1000')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Verify response structure
        assert data['success'] is True
        assert data['count'] == 3
        assert len(data['places']) == 3
        
        # Verify first place data
        first_place = data['places'][0]
        assert first_place['name'] == 'Le Petit Bistrot'
        assert first_place['address'] == '123 Rue de la Paix, 75001 Paris, France'
        assert first_place['phone'] == '+33 1 23 45 67 89'
        assert first_place['email'] is None
        assert first_place['type'] == 'restaurant'
        assert first_place['geo']['latitude'] == 48.8566
        assert first_place['geo']['longitude'] == 2.3522
        
        # Verify search parameters
        assert data['searchParams']['latitude'] == 48.8566
        assert data['searchParams']['longitude'] == 2.3522
        assert data['searchParams']['type'] == 'restaurant'
        assert data['searchParams']['radius'] == 1000.0

    def test_get_places_missing_required_params(self, client):
        """Test places search with missing required parameters."""
        # Test without latitude
        response = client.get('/google_places/places?longitude=2.3522')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "latitude and longitude are required" in data['error']
        
        # Test without longitude
        response = client.get('/google_places/places?latitude=48.8566')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "latitude and longitude are required" in data['error']

    def test_get_places_invalid_coordinates(self, client):
        """Test places search with invalid coordinate values."""
        # Test with non-numeric latitude
        response = client.get('/google_places/places?latitude=invalid&longitude=2.3522')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "latitude and longitude must be valid numbers" in data['error']
        
        # Test with non-numeric longitude
        response = client.get('/google_places/places?latitude=48.8566&longitude=invalid')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "latitude and longitude must be valid numbers" in data['error']

    def test_get_places_default_parameters(self, client, mock_requests_post, mock_google_places_response):
        """Test places search with default parameters."""
        # Mock the successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_google_places_response
        mock_requests_post.return_value = mock_response

        # Test with only required parameters
        with patch.dict('os.environ', {'GOOGLE_API_KEY': 'fake-api-key'}):
            response = client.get('/google_places/places?latitude=48.8566&longitude=2.3522')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Verify default values are used
        assert data['searchParams']['type'] == 'restaurant'  # default
        assert data['searchParams']['radius'] == 1000.0  # default
        assert len(data['places']) <= 20  # default maxResults

    def test_get_places_different_type(self, client, mock_requests_post, mock_google_places_response):
        """Test places search with different place type."""
        # Mock the successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_google_places_response
        mock_requests_post.return_value = mock_response

        # Test with cafe type
        with patch.dict('os.environ', {'GOOGLE_API_KEY': 'fake-api-key'}):
            response = client.get('/google_places/places?latitude=48.8566&longitude=2.3522&type=cafe')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['searchParams']['type'] == 'cafe'

    def test_get_places_api_error(self, client, mock_requests_post, mock_google_places_error_response):
        """Test places search when Google Places API returns an error."""
        # Mock the error response
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = json.dumps(mock_google_places_error_response)
        mock_requests_post.return_value = mock_response

        with patch.dict('os.environ', {'GOOGLE_API_KEY': 'fake-api-key'}):
            response = client.get('/google_places/places?latitude=48.8566&longitude=2.3522')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert data['status_code'] == 400

    def test_get_places_empty_response(self, client, mock_requests_post):
        """Test places search when no places are found."""
        # Mock empty response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"places": []}
        mock_requests_post.return_value = mock_response

        with patch.dict('os.environ', {'GOOGLE_API_KEY': 'fake-api-key'}):
            response = client.get('/google_places/places?latitude=48.8566&longitude=2.3522')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['count'] == 0
        assert len(data['places']) == 0

    def test_get_places_missing_phone_number(self, client, mock_requests_post):
        """Test places search with places that don't have phone numbers."""
        # Mock response with missing phone numbers
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "places": [
                {
                    "displayName": {
                        "text": "Restaurant Sans Téléphone",
                        "languageCode": "fr"
                    },
                    "formattedAddress": "456 Rue Sans Téléphone, Paris, France",
                    "location": {
                        "latitude": 48.8566,
                        "longitude": 2.3522
                    },
                    "types": ["restaurant", "food", "establishment"]
                }
            ]
        }
        mock_requests_post.return_value = mock_response

        with patch.dict('os.environ', {'GOOGLE_API_KEY': 'fake-api-key'}):
            response = client.get('/google_places/places?latitude=48.8566&longitude=2.3522')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['places'][0]['phone'] is None

    def test_get_places_custom_radius_and_max_results(self, client, mock_requests_post, mock_google_places_response):
        """Test places search with custom radius and maxResults."""
        # Mock the successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_google_places_response
        mock_requests_post.return_value = mock_response

        # Test with custom parameters
        with patch.dict('os.environ', {'GOOGLE_API_KEY': 'fake-api-key'}):
            response = client.get('/google_places/places?latitude=48.8566&longitude=2.3522&radius=500&maxResults=5')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['searchParams']['radius'] == 500.0
        # Note: maxResults is not returned in searchParams, only used internally

    def test_get_places_missing_api_key(self, client):
        """Test places search when GOOGLE_API_KEY is missing."""
        with patch.dict('os.environ', {}, clear=True):
            response = client.get('/google_places/places?latitude=48.8566&longitude=2.3522')
            
            assert response.status_code == 500
            data = json.loads(response.data)
            assert "Missing GOOGLE_API_KEY" in data['error']

    def test_health_check_endpoint(self, client):
        """Test the health check endpoint."""
        response = client.get('/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['service'] == 'prospects-flow-service' 