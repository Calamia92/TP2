from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import UserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Vue pour l'inscription d'un nouvel utilisateur.
    """
    try:
        data = request.data
        
        # Validation des données
        if not all([data.get('username'), data.get('password'), data.get('email')]):
            return Response(
                {'error': 'Username, password et email sont requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Vérifier si l'utilisateur existe déjà
        if User.objects.filter(username=data['username']).exists():
            return Response(
                {'error': 'Un utilisateur avec ce nom existe déjà'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(email=data['email']).exists():
            return Response(
                {'error': 'Un utilisateur avec cet email existe déjà'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Créer l'utilisateur
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', '')
        )
        
        # Générer les tokens JWT
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Utilisateur créé avec succès',
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': 'Erreur lors de la création de l\'utilisateur'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Vue pour la connexion d'un utilisateur.
    """
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Username et password sont requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Authentifier l'utilisateur
        user = authenticate(username=username, password=password)
        
        if user is None:
            return Response(
                {'error': 'Identifiants invalides'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Générer les tokens JWT
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Connexion réussie',
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
        
    except Exception as e:
        return Response(
            {'error': 'Erreur lors de la connexion'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def logout(request):
    """
    Vue pour la déconnexion d'un utilisateur.
    """
    try:
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return Response(
                {'error': 'Le token refresh est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Blacklister le token
        token = RefreshToken(refresh_token)
        token.blacklist()
        
        return Response({'message': 'Déconnexion réussie'})
        
    except Exception as e:
        return Response(
            {'error': 'Erreur lors de la déconnexion'},
            status=status.HTTP_400_BAD_REQUEST
        )