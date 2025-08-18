from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    """
    Permission personnalisée pour permettre seulement aux propriétaires
    d'une tâche de la modifier ou la supprimer.
    """

    def has_object_permission(self, request, view, obj):
        # Permissions de lecture pour tous les utilisateurs authentifiés
        if request.method in ['GET']:
            return True
            
        # Permissions d'écriture seulement pour le propriétaire de la tâche
        return obj.owner == request.user