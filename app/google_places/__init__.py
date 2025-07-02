from flask import Blueprint
from flask_restx import Api, Resource, fields

google_places = Blueprint('google_places', __name__)

# Créer l'API Swagger pour ce blueprint
api = Api(
    google_places,
    version='1.0',
    title='Google Places API',
    description='API pour récupérer les lieux via Google Places API',
    doc='/swagger-docs/',
    default='google_places',
    default_label='Google Places Endpoints'
)

# Définir les modèles de données pour Swagger
place_model = api.model('Place', {
    'name': fields.String(description='Nom du lieu'),
    'address': fields.String(description='Adresse du lieu'),
    'phone': fields.String(description='Numéro de téléphone'),
    'email': fields.String(description='Email (non disponible via Google Places)'),
    'type': fields.String(description='Type de lieu'),
    'geo': fields.Nested(api.model('Geo', {
        'latitude': fields.Float(description='Latitude'),
        'longitude': fields.Float(description='Longitude')
    }))
})

places_response = api.model('PlacesResponse', {
    'success': fields.Boolean(description='Statut de la requête'),
    'count': fields.Integer(description='Nombre de lieux trouvés'),
    'places': fields.List(fields.Nested(place_model), description='Liste des lieux'),
    'searchParams': fields.Nested(api.model('SearchParams', {
        'latitude': fields.Float(description='Latitude de recherche'),
        'longitude': fields.Float(description='Longitude de recherche'),
        'type': fields.String(description='Type de lieu recherché'),
        'radius': fields.Float(description='Rayon de recherche en mètres')
    }))
})

from app.google_places import routes