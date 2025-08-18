from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Task
from .serializers import TaskSerializer, TaskCreateSerializer, TaskUpdateSerializer
from .permissions import IsOwnerOrReadOnly

class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet complet pour les opérations CRUD sur les tâches.
    Permet la création, lecture, mise à jour et suppression des tâches.
    """
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'priority']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'due_date', 'priority']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """
        Retourne la classe de serializer appropriée selon l'action.
        """
        if self.action == 'create':
            return TaskCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TaskUpdateSerializer
        return TaskSerializer
    
    def get_queryset(self):
        """
        Retourne uniquement les tâches de l'utilisateur connecté.
        """
        return Task.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        """
        Assigne automatiquement l'utilisateur connecté comme propriétaire.
        """
        serializer.save(owner=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_tasks(self, request):
        """
        Action personnalisée pour récupérer toutes les tâches de l'utilisateur.
        """
        tasks = self.get_queryset()
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """
        Action personnalisée pour filtrer les tâches par statut.
        """
        status_param = request.query_params.get('status')
        if status_param:
            tasks = self.get_queryset().filter(status=status_param)
            serializer = self.get_serializer(tasks, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'Le paramètre status est requis'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['patch'])
    def mark_as_done(self, request, pk=None):
        """
        Action personnalisée pour marquer une tâche comme terminée.
        """
        task = self.get_object()
        task.status = 'done'
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
