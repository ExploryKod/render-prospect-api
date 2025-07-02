# Tests Unitaires - Render Prospects Flow

Ce document explique comment exécuter les tests unitaires pour l'application Render Prospects Flow.

## Structure des Tests

```
tests/
├── __init__.py
├── conftest.py                    # Configuration pytest et fixtures
├── test_google_places_routes.py   # Tests pour les routes Google Places
└── test_llm_routes.py            # Tests pour les routes LLM
```

## Installation et Exécution

### 1. Installer les dépendances de test

```bash
pip install -r requirements.txt
```

### 2. Exécuter tous les tests

```bash
pytest
```

### 3. Exécuter les tests avec couverture

```bash
pytest --cov=app --cov-report=html
```

### 4. Exécuter un test spécifique

```bash
pytest tests/test_google_places_routes.py::TestGooglePlacesRoutes::test_get_places_success -v
```

### 5. Exécuter les tests en mode verbose

```bash
pytest -v
```

## Mocks et Fixtures

### Mock Google Places API

Les tests utilisent des mocks pour éviter d'appeler l'API Google Places (coûteuse) :

- **mock_google_places_response** : Simule une réponse réussie de l'API
- **mock_google_places_error_response** : Simule une erreur de l'API
- **mock_requests_post** : Mock de la fonction `requests.post`

### Données de Test

Les données de test incluent :
- 3 restaurants parisiens avec coordonnées réelles
- Informations complètes : nom, adresse, téléphone, géolocalisation
- Gestion des cas d'erreur et des réponses vides

## Tests Disponibles

### Tests Google Places Routes

1. **test_get_places_success** : Test de recherche réussie
2. **test_get_places_missing_required_params** : Test des paramètres manquants
3. **test_get_places_invalid_coordinates** : Test des coordonnées invalides
4. **test_get_places_default_parameters** : Test des paramètres par défaut
5. **test_get_places_different_type** : Test avec différents types de lieux
6. **test_get_places_api_error** : Test des erreurs API
7. **test_get_places_empty_response** : Test des réponses vides
8. **test_get_places_missing_phone_number** : Test des numéros manquants
9. **test_get_places_custom_radius_and_max_results** : Test des paramètres personnalisés
10. **test_health_check_endpoint** : Test de l'endpoint de santé

### Tests LLM Routes

1. **test_llm_endpoints_exist** : Vérification de l'existence des endpoints LLM

## Configuration

Le fichier `pytest.ini` configure :
- Répertoire des tests : `tests/`
- Fichiers de test : `test_*.py`
- Classes de test : `Test*`
- Fonctions de test : `test_*`
- Couverture de code avec rapports HTML et XML
- Marqueurs pour catégoriser les tests

## Avantages des Mocks

1. **Économique** : Pas d'appels à l'API Google Places (coûteuse)
2. **Rapide** : Tests instantanés sans latence réseau
3. **Prévisible** : Réponses contrôlées et reproductibles
4. **Isolé** : Tests indépendants de l'état externe
5. **Complet** : Test de tous les cas d'usage et d'erreur

## Exemple de Données Mock

```json
{
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
      "types": ["restaurant", "food", "establishment"]
    }
  ]
}
```

## Intégration Continue

Ces tests peuvent être intégrés dans un pipeline CI/CD pour :
- Vérifier la qualité du code
- Détecter les régressions
- Assurer la couverture de code
- Valider les modifications avant déploiement 