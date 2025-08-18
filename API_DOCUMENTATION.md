# API Documentation - Task Management System

## Vue d'ensemble
Cette API Django REST Framework fournit une gestion complète des tâches avec authentification JWT et permissions.

## Authentification

### 1. Inscription d'un utilisateur
```
POST /auth/register/
Content-Type: application/json

{
    "username": "testuser",
    "email": "test@example.com",
    "password": "motdepasse123",
    "first_name": "John", // optionnel
    "last_name": "Doe"    // optionnel
}
```

**Réponse:**
```json
{
    "message": "Utilisateur créé avec succès",
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "John",
        "last_name": "Doe"
    },
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 2. Connexion
```
POST /auth/login/
Content-Type: application/json

{
    "username": "testuser",
    "password": "motdepasse123"
}
```

### 3. Déconnexion
```
POST /auth/logout/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "refresh": "<refresh_token>"
}
```

### 4. Rafraîchir le token
```
POST /auth/token/refresh/
Content-Type: application/json

{
    "refresh": "<refresh_token>"
}
```

## Gestion des Tâches

**Note:** Toutes les requêtes nécessitent l'authentification:
```
Authorization: Bearer <access_token>
```

### 1. Lister toutes les tâches de l'utilisateur
```
GET /api/tasks/
```

**Paramètres de requête:**
- `status`: Filtrer par statut (todo, in_progress, done)
- `priority`: Filtrer par priorité (low, medium, high)
- `search`: Rechercher dans le titre et la description
- `ordering`: Trier par champ (-created_at, updated_at, due_date, priority)
- `page`: Numéro de page (pagination)

**Exemple:**
```
GET /api/tasks/?status=todo&priority=high&search=urgent&ordering=-created_at
```

### 2. Créer une nouvelle tâche
```
POST /api/tasks/
Content-Type: application/json

{
    "title": "Ma nouvelle tâche",
    "description": "Description détaillée",
    "priority": "high",
    "status": "todo",
    "due_date": "2025-08-20T10:00:00Z" // optionnel
}
```

### 3. Récupérer une tâche spécifique
```
GET /api/tasks/{id}/
```

### 4. Mettre à jour une tâche
```
PUT /api/tasks/{id}/
Content-Type: application/json

{
    "title": "Titre modifié",
    "description": "Description modifiée",
    "priority": "medium",
    "status": "in_progress",
    "due_date": "2025-08-25T15:30:00Z"
}
```

**Ou mise à jour partielle:**
```
PATCH /api/tasks/{id}/
Content-Type: application/json

{
    "status": "done"
}
```

### 5. Supprimer une tâche
```
DELETE /api/tasks/{id}/
```

### Actions personnalisées

#### Récupérer ses tâches
```
GET /api/tasks/my_tasks/
```

#### Filtrer par statut
```
GET /api/tasks/by_status/?status=todo
```

#### Marquer comme terminé
```
PATCH /api/tasks/{id}/mark_as_done/
```

## Exemples de réponses

### Tâche complète
```json
{
    "id": 1,
    "title": "Finaliser le projet",
    "description": "Terminer toutes les fonctionnalités",
    "priority": "high",
    "status": "in_progress",
    "created_at": "2025-08-18T10:00:00Z",
    "updated_at": "2025-08-18T14:30:00Z",
    "due_date": "2025-08-20T17:00:00Z",
    "owner": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "John",
        "last_name": "Doe"
    }
}
```

### Liste paginée
```json
{
    "count": 25,
    "next": "http://localhost:8000/api/tasks/?page=2",
    "previous": null,
    "results": [
        // ... tâches
    ]
}
```

## Codes de statut HTTP

- `200 OK`: Succès
- `201 Created`: Ressource créée
- `400 Bad Request`: Données invalides
- `401 Unauthorized`: Non authentifié
- `403 Forbidden`: Pas d'autorisation
- `404 Not Found`: Ressource introuvable
- `500 Internal Server Error`: Erreur serveur

## Sécurité et Permissions

- **Authentification JWT**: Requis pour toutes les opérations sur les tâches
- **Propriété**: Les utilisateurs ne peuvent voir/modifier que leurs propres tâches
- **Validation**: Tous les champs sont validés côté serveur
- **CORS**: Configuré pour les requêtes cross-origin (en développement)

## Modèle de données

### Task
- `id`: Identifiant unique (auto-généré)
- `title`: Titre (obligatoire, min 3 caractères)
- `description`: Description (optionnel)
- `priority`: Priorité (low, medium, high)
- `status`: Statut (todo, in_progress, done)
- `created_at`: Date de création (auto)
- `updated_at`: Date de modification (auto)
- `due_date`: Date d'échéance (optionnel)
- `owner`: Propriétaire (utilisateur connecté)

### User
- Utilise le modèle User standard de Django
- Champs disponibles: username, email, first_name, last_name