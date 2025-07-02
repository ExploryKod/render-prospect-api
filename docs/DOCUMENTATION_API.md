# Documentation API - Service de Flux de Prospects

## Vue d'ensemble

Le Service de Flux de Prospects fournit une API complète pour la planification de tournées commerciales avec intégration à plusieurs sources de données, incluant Google Places et les données d'entreprises du gouvernement français.

**URL de base :** `http://localhost:5000`  
**Type de contenu :** `application/json`  
**Authentification :** Aucune requise (API publique)

## Limites de taux

- **API Entreprises Françaises :** 7 requêtes/seconde
- **API Google Places :** Selon les quotas Google
- **API Générale :** Aucune limite spécifique

## Points de terminaison

### Vérification de santé

#### GET `/health`

Vérifier le statut de santé du service.

**Réponse :**
```json
{
  "status": "healthy",
  "service": "prospects-flow-service"
}
```

**Codes de statut :**
- `200` - Service en bonne santé

---
### Intégration Google Places

#### GET `/google_places/search`

Rechercher des lieux en utilisant l'API Google Places.

**Paramètres de requête :**

| Paramètre | Type | Requis | Description | Exemple |
|-----------|------|--------|-------------|---------|
| `query` | string | Oui | Terme de recherche | `"restaurant"` |
| `location` | string | Non | Localisation (lat,lng) | `"48.8566,2.3522"` |
| `radius` | integer | Non | Rayon de recherche en mètres | `5000` |
| `type` | string | Non | Type de lieu | `"restaurant"` |

**Exemple de requête :**
```bash
curl "http://localhost:5000/google_places/search?query=restaurant&location=48.8566,2.3522&radius=5000"
```

**Exemple de réponse :**
```json
{
  "status": "OK",
  "results": [
    {
      "place_id": "ChIJN1t_tDeuEmsRUsoyG83frY4",
      "name": "Le Petit Bistrot",
      "formatted_address": "15 Rue de Rivoli, 75001 Paris, France",
      "geometry": {
        "location": {
          "lat": 48.8566,
          "lng": 2.3522
        }
      },
      "types": ["restaurant", "food", "establishment"]
    }
  ]
}
```

**Codes de statut :**
- `200` - Succès
- `400` - Requête incorrecte
- `500` - Erreur interne du serveur

### Recherche d'entreprises françaises

#### GET `/gov_places/enterprises/search`

Rechercher des entreprises françaises selon différents critères.

**Paramètres de requête :**

| Paramètre | Type | Requis | Description | Exemple |
|-----------|------|--------|-------------|---------|
| `q` | string | Oui | Terme de recherche (nom d'entreprise, adresse, dirigeants) | `"restaurant"` |
| `code_postal` | string | Non | Filtrer par code postal | `"75001"` |
| `code_naf` | string | Non | Filtrer par code NAF d'activité | `"47.11Z"` |
| `effectif_min` | integer | Non | Nombre minimum d'employés | `10` |
| `effectif_max` | integer | Non | Nombre maximum d'employés | `100` |
| `entreprises_individuelles` | boolean | Non | Entreprises individuelles uniquement | `true` |

**Exemple de requête :**
```bash
curl "http://localhost:5000/gov_places/enterprises/search?q=restaurant&code_postal=75001&effectif_min=10"
```

**Exemple de réponse :**
```json
{
  "query": "restaurant",
  "filters_applied": {
    "code_postal": "75001",
    "effectif_min": "10"
  },
  "total_results": 25,
  "timestamp": "2024-01-15T10:30:00.000Z",
  "results": [
    {
      "denomination": "LE PETIT BISTROT",
      "siren": "123456789",
      "siret": "12345678900012",
      "code_naf": "56.10A",
      "effectif": "10-19",
      "adresse": {
        "numero": "15",
        "voie": "RUE DE RIVOLI",
        "code_postal": "75001",
        "commune": "PARIS"
      }
    }
  ]
}
```

**Codes de statut :**
- `200` - Succès
- `400` - Requête incorrecte (paramètres manquants ou invalides)
- `408` - Délai d'attente dépassé (limite de taux dépassée)
- `500` - Erreur interne du serveur

---

#### GET `/gov_places/enterprises/{siren}`

Obtenir les informations détaillées d'une entreprise spécifique par numéro SIREN.

**Paramètres de chemin :**

| Paramètre | Type | Requis | Description | Exemple |
|-----------|------|--------|-------------|---------|
| `siren` | string | Oui | Numéro SIREN à 9 chiffres | `"380129867"` |

**Exemple de requête :**
```bash
curl "http://localhost:5000/gov_places/enterprises/380129867"
```

**Exemple de réponse :**
```json
{
  "siren": "380129867",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "enterprise": {
    "denomination": "ORANGE",
    "siren": "380129867",
    "siret": "38012986700034",
    "code_naf": "61.20Z",
    "libelle_naf": "Télécommunications filaires",
    "effectif": "10000+",
    "date_creation": "1987-12-31",
    "adresse": {
      "numero": "78",
      "voie": "RUE OLIVIER DE SERRES",
      "code_postal": "75015",
      "commune": "PARIS",
      "departement": "75",
      "region": "ILE-DE-FRANCE"
    }
  }
}
```

**Codes de statut :**
- `200` - Succès
- `400` - Format SIREN invalide
- `404` - Entreprise non trouvée
- `408` - Délai d'attente dépassé
- `500` - Erreur interne du serveur

---

#### GET `/gov_places/enterprises/geographic`

Rechercher des entreprises dans une zone géographique spécifique.

**Paramètres de requête :**

| Paramètre | Type | Requis | Description | Exemple |
|-----------|------|--------|-------------|---------|
| `lat` | float | Oui | Coordonnée de latitude | `48.8566` |
| `lon` | float | Oui | Coordonnée de longitude | `2.3522` |
| `radius` | integer | Non | Rayon de recherche en mètres (défaut: 1000) | `2000` |

**Exemple de requête :**
```bash
curl "http://localhost:5000/gov_places/enterprises/geographic?lat=48.8566&lon=2.3522&radius=2000"
```

**Exemple de réponse :**
```json
{
  "location": {
    "lat": "48.8566",
    "lon": "2.3522",
    "radius": "2000"
  },
  "total_results": 45,
  "timestamp": "2024-01-15T10:30:00.000Z",
  "results": [
    {
      "denomination": "CAFE DE FLORE",
      "siren": "123456789",
      "distance": 150,
      "adresse": {
        "voie": "BOULEVARD SAINT-GERMAIN",
        "code_postal": "75006",
        "commune": "PARIS"
      }
    }
  ]
}
```

**Codes de statut :**
- `200` - Succès
- `400` - Paramètres requis manquants
- `408` - Délai d'attente dépassé
- `500` - Erreur interne du serveur

---



---

### Services LLM

#### GET `/llm/health`

Vérifier la santé du service LLM.

**Exemple de requête :**
```bash
curl "http://localhost:5000/llm/health"
```

**Exemple de réponse :**
```json
{
  "status": "healthy",
  "service": "llm-service"
}
```

**Codes de statut :**
- `200` - Service en bonne santé
- `503` - Service indisponible

---

## Modèles de données

### Objet Entreprise

```json
{
  "denomination": "string",
  "siren": "string (9 chiffres)",
  "siret": "string (14 chiffres)",
  "code_naf": "string",
  "libelle_naf": "string",
  "effectif": "string",
  "date_creation": "string (YYYY-MM-DD)",
  "adresse": {
    "numero": "string",
    "voie": "string",
    "code_postal": "string",
    "commune": "string",
    "departement": "string",
    "region": "string"
  }
}
```

### Objet Adresse

```json
{
  "numero": "string",
  "voie": "string",
  "code_postal": "string",
  "commune": "string",
  "departement": "string",
  "region": "string"
}
```

### Réponse de recherche

```json
{
  "query": "string",
  "filters_applied": "object",
  "total_results": "integer",
  "timestamp": "string (ISO 8601)",
  "results": "array"
}
```

---

## Réponses d'erreur

### Format d'erreur standard

```json
{
  "error": "string",
  "details": "string (optionnel)",
  "timestamp": "string (ISO 8601)"
}
```

### Codes d'erreur courants

| Code de statut | Type d'erreur | Description |
|----------------|---------------|-------------|
| `400` | Requête incorrecte | Paramètres manquants ou invalides |
| `404` | Non trouvé | Ressource non trouvée |
| `408` | Délai d'attente dépassé | Limite de taux dépassée ou timeout |
| `500` | Erreur interne du serveur | Erreur serveur |

---

## Codes NAF courants

| Code | Description |
|------|-------------|
| `47.11Z` | Commerce de détail en magasin non spécialisé |
| `47.21Z` | Commerce de détail de fruits et légumes |
| `47.22Z` | Commerce de détail de viandes et de produits à base de viande |
| `47.23Z` | Commerce de détail de poissons, crustacés et mollusques |
| `47.24Z` | Commerce de détail de pain, pâtisserie et confiserie |
| `47.25Z` | Commerce de détail de boissons |
| `47.26Z` | Commerce de détail de produits à base de tabac |
| `47.29Z` | Autre commerce de détail alimentaire spécialisé |
| `47.30Z` | Commerce de détail de carburants |
| `47.41Z` | Commerce de détail d'ordinateurs, d'unités périphériques et de logiciels |
| `47.42Z` | Commerce de détail de matériels de télécommunication |
| `47.43Z` | Commerce de détail de matériels audio et vidéo |
| `47.51Z` | Commerce de détail de textiles |
| `47.52Z` | Commerce de détail de quincaillerie, peintures et verres |
| `47.53Z` | Commerce de détail de tapis, luminaires et appareils ménagers |
| `47.54Z` | Commerce de détail d'appareils électroménagers |
| `47.59Z` | Commerce de détail de meubles, articles d'éclairage et autres articles de ménage |
| `47.61Z` | Commerce de détail de livres |
| `47.62Z` | Commerce de détail de journaux et papeterie |
| `47.63Z` | Commerce de détail d'enregistrements musicaux et vidéo |
| `47.64Z` | Commerce de détail d'articles de sport |
| `47.65Z` | Commerce de détail de jeux et jouets |
| `47.71Z` | Commerce de détail d'habillement |
| `47.72Z` | Commerce de détail de chaussures et d'articles en cuir |
| `47.73Z` | Commerce de détail de produits pharmaceutiques |
| `47.74Z` | Commerce de détail d'articles médicaux et orthopédiques |
| `47.75Z` | Commerce de détail de parfumerie et de produits de beauté |
| `47.76Z` | Commerce de détail de fleurs, plantes, graines, engrais, animaux de compagnie et aliments pour ces animaux |
| `47.77Z` | Commerce de détail d'articles d'horlogerie et de bijouterie |
| `47.78Z` | Autre commerce de détail de biens neufs en magasin spécialisé |
| `47.79Z` | Commerce de détail de biens d'occasion en magasin |
| `47.81Z` | Commerce de détail sur éventaires et marchés de produits alimentaires, boissons et tabac |
| `47.82Z` | Commerce de détail sur éventaires et marchés de textiles, d'habillement et de chaussures |
| `47.89Z` | Commerce de détail sur éventaires et marchés d'autres produits |
| `47.91Z` | Commerce de détail par correspondance ou par Internet |
| `47.99Z` | Autre commerce de détail hors magasin, éventaires ou marchés |
| `62.01Z` | Programmation informatique |
| `62.02Z` | Conseil informatique |
| `62.03Z` | Gestion d'installations informatiques |
| `62.09Z` | Autres activités informatiques |

---

## Exemples d'utilisation

### Recherche de restaurants à Paris

```bash
curl "http://localhost:5000/gov_places/enterprises/search?q=restaurant&code_postal=75001&effectif_min=5"
```

### Recherche d'entreprises technologiques

```bash
curl "http://localhost:5000/gov_places/enterprises/search?q=informatique&code_naf=62.01Z"
```

### Recherche géographique autour de la Tour Eiffel

```bash
curl "http://localhost:5000/gov_places/enterprises/geographic?lat=48.8584&lon=2.2945&radius=1000"
```

### Obtenir les détails d'une entreprise spécifique

```bash
curl "http://localhost:5000/gov_places/enterprises/380129867"
```

### Recherche de lieux avec Google Places

```bash
curl "http://localhost:5000/google_places/search?query=cafe&location=48.8566,2.3522&radius=2000"
```

---

## Bonnes pratiques

### 1. Gestion des limites de taux
- Implémentez des délais entre les requêtes (minimum 143ms entre les appels)
- Utilisez un backoff exponentiel pour les nouvelles tentatives
- Surveillez les en-têtes de réponse pour les informations de limite de taux

### 2. Optimisation des recherches
- Utilisez des termes de recherche spécifiques pour de meilleurs résultats
- Combinez plusieurs filtres pour affiner les résultats
- Utilisez les codes NAF pour les recherches spécifiques à l'industrie

### 3. Gestion des erreurs
- Gérez toujours les erreurs de timeout gracieusement
- Implémentez une logique de nouvelle tentative avec backoff exponentiel
- Enregistrez les erreurs API pour la surveillance

### 4. Mise en cache des données
- Envisagez de mettre en cache les données fréquemment demandées
- Implémentez des stratégies d'invalidation du cache
- Respectez les exigences de fraîcheur des données

---

## Support et ressources

- **Documentation API officielle :** [data.gouv.fr](https://www.data.gouv.fr/fr/dataservices/api-recherche-dentreprises/)
- **Base de données SIRENE :** [INSEE](https://www.insee.fr/fr/information/4190491)
- **Codes NAF :** [INSEE NAF](https://www.insee.fr/fr/metadonnees/nafr2/sous-classe)

---

## Journal des modifications

### Version 1.0.0 (15/01/2024)
- Implémentation initiale
- Support de la recherche textuelle
- Support de la recherche géographique
- Support de la recherche par SIREN
- Capacités de filtrage de base 