import pytest
import os
from unittest.mock import patch
from app import create_app

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def mock_google_places_response():
    """Mock response data that mimics Google Places API response."""
    return {
        "places": [
            {
                "displayName": {
                    "text": "Le Petit Bistrot",
                    "languageCode": "fr"
                },
                "formattedAddress": "123 Rue de la Paix, 75001 Paris, France",
                "location": {
                    "latitude": 48.8566,
                    "longitude": 2.3522
                },
                "nationalPhoneNumber": "+33 1 23 45 67 89",
                "internationalPhoneNumber": "+33 1 23 45 67 89",
                "types": ["restaurant", "food", "establishment"]
            },
            {
                "displayName": {
                    "text": "Café de Flore",
                    "languageCode": "fr"
                },
                "formattedAddress": "172 Boulevard Saint-Germain, 75006 Paris, France",
                "location": {
                    "latitude": 48.8534,
                    "longitude": 2.3348
                },
                "nationalPhoneNumber": "+33 1 45 48 55 26",
                "internationalPhoneNumber": "+33 1 45 48 55 26",
                "types": ["cafe", "food", "establishment"]
            },
            {
                "displayName": {
                    "text": "L'Ami Louis",
                    "languageCode": "fr"
                },
                "formattedAddress": "32 Rue du Vertbois, 75003 Paris, France",
                "location": {
                    "latitude": 48.8647,
                    "longitude": 2.3622
                },
                "nationalPhoneNumber": "+33 1 48 87 77 48",
                "internationalPhoneNumber": "+33 1 48 87 77 48",
                "types": ["restaurant", "food", "establishment"]
            }
        ]
    }

@pytest.fixture
def mock_google_places_error_response():
    """Mock error response from Google Places API."""
    return {
        "error": {
            "code": 400,
            "message": "Invalid request",
            "status": "INVALID_ARGUMENT"
        }
    }

@pytest.fixture
def mock_requests_post():
    """Mock for requests.post to avoid real API calls."""
    with patch('app.google_places.routes.requests.post') as mock_post:
        yield mock_post 