# Task Management API

Une API REST simple pour gérer vos tâches avec authentification sécurisée.

## 🚀 Démarrage rapide

### 1. Installation
```bash
# Installer les dépendances
pip install -r requirements.txt

# Créer la base de données
python manage.py migrate

# Créer un compte admin (optionnel)
python manage.py createsuperuser

# Démarrer le serveur
python manage.py runserver
```

L'API sera disponible sur `http://127.0.0.1:8000/`

### 2. Premier test
```bash
# S'inscrire
curl -X POST http://127.0.0.1:8000/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"monnom","email":"test@email.com","password":"monmotdepasse"}'

# Se connecter
curl -X POST http://127.0.0.1:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"monnom","password":"monmotdepasse"}'
```

## 📋 Fonctionnalités

- ✅ **Inscription/Connexion** sécurisée avec JWT
- ✅ **Créer, modifier, supprimer** des tâches
- ✅ **Filtrer** par statut (todo, en cours, terminé)
- ✅ **Filtrer** par priorité (basse, moyenne, haute)
- ✅ **Rechercher** dans les tâches
- ✅ **Pagination** automatique
- ✅ **Permissions** : chacun ne voit que ses tâches

## 🔧 Utilisation

### S'authentifier
1. **S'inscrire** : `POST /auth/register/`
2. **Se connecter** : `POST /auth/login/`
3. **Utiliser le token** dans vos requêtes : `Authorization: Bearer <votre-token>`

### Gérer les tâches
- **Voir toutes mes tâches** : `GET /api/tasks/`
- **Créer une tâche** : `POST /api/tasks/`
- **Modifier une tâche** : `PUT /api/tasks/1/`
- **Supprimer une tâche** : `DELETE /api/tasks/1/`

### Exemples
```bash
# Créer une tâche (remplacez YOUR_TOKEN)
curl -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Faire les courses","priority":"high","status":"todo"}'

# Voir toutes mes tâches
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8000/api/tasks/

# Filtrer les tâches urgentes
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://127.0.0.1:8000/api/tasks/?priority=high"
```

## 📚 Documentation complète

Voir le fichier `API_DOCUMENTATION.md` pour tous les détails.

## 🛠️ Technologies

- **Django** 5.2.5
- **Django REST Framework** 3.15.2
- **JWT Authentication** (Simple JWT)
- **SQLite** (base de données)

## 📁 Structure du projet

```
TP2/
├── TP2/                    # Configuration Django
├── tasks/                  # Application principale
│   ├── models.py          # Modèle Task
│   ├── views.py           # API endpoints
│   ├── serializers.py     # Validation données
│   └── permissions.py     # Sécurité
├── requirements.txt       # Dépendances
└── README.md             # Ce fichier
```

## 🔒 Sécurité

- Authentification JWT obligatoire
- Chaque utilisateur ne peut voir que ses propres tâches
- Validation de toutes les données d'entrée
- Permissions personnalisées