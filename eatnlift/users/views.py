from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status

from django.contrib.auth.models import User
from .models import CustomUser

from .serializer import UserSerializer, UserProfileSerializer

from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

@api_view(['POST'])
def signin(request):
    errors = []

    if 'username' not in request.data:
        errors.append("Es requereix el nom d'usuari")
    if 'email' not in request.data:
        errors.append("Es requereix el correu electrònic")
    else:
        email_validator = EmailValidator()
        try:
            email_validator(request.data['email'])
        except ValidationError:
            errors.append("El correu electrònic no és vàlid")
    if 'password' not in request.data:
        errors.append("Es requereix la contrasenya")

    if errors:
        return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)


    if CustomUser.objects.filter(username=request.data['username']).exists():
        return Response({"errors": ["L'usuari ja existeix"]}, status=status.HTTP_400_BAD_REQUEST)
    if CustomUser.objects.filter(email=request.data["email"]).exists():
        return Response({"errors": ["El correu electrònic ja està en ús"]}, status=status.HTTP_400_BAD_REQUEST)

    user = CustomUser(username=request.data["username"], email=request.data["email"])
    user.set_password(request.data["password"])
    user.save()

    token = Token.objects.create(user=user)

    serializer = UserSerializer(user)

    return Response({'token': token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    errors = []
    user = None

    if 'username' not in request.data:
        errors.append("Es requereix el nom d'usuari")
    else:
        user = CustomUser.objects.filter(username=request.data['username']).first()
        if not user:
            errors.append("L'usuari no existeix")
    

    if 'password' not in request.data:
        errors.append("Es requereix la contrasenya")
    elif user and not user.check_password(request.data['password']):
        errors.append("La contrasenya és incorrecta")

    if errors:
        return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)

    return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def googleLogin(request):
    google_token = request.data.get('google_token')
    if not google_token:
        return Response({"errors": ["No token provided"]}, status=status.HTTP_400_BAD_REQUEST)

    try:
        idinfo = id_token.verify_oauth2_token(
            google_token,
            google_requests.Request(),
            "73227425624-ffg6valiprbvrkpb46riqu3on8jm25uu.apps.googleusercontent.com"
        )

        print(idinfo)
        google_email = idinfo.get('email')
        google_username = google_email.split('@')[0]
        google_picture = idinfo.get('picture')

        try:
            user = CustomUser.objects.get(email=google_email)
        except CustomUser.DoesNotExist:
            user = CustomUser(username=google_username, email=google_email)
            user.save()

        if google_picture:
            user.picture = google_picture
            user.save()

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
        }, status=status.HTTP_200_OK)

    except ValueError:
        return Response({"errors": ["Invalid token"]}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get(request, id):
    errors = []
    
    try:
        user = CustomUser.objects.get(id=id)
    except:
        return Response({"errors": ["L'usuari no existeix"]}, status=status.HTTP_404_NOT_FOUND) 

    serializer = UserSerializer(instance=user)
    return Response({"user": serializer.data}, status=status.HTTP_200_OK)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def editPersonalInformation(request, id):
    try:
        user = CustomUser.objects.get(id=id)
    except CustomUser.DoesNotExist:
        return Response({"errors": ["L'usuari no existeix."]}, status=status.HTTP_404_NOT_FOUND)

    if request.user != user:
        return Response({"errors": ["No tens permís per actualitzar aquesta informació personal."]}, status=status.HTTP_403_FORBIDDEN)

    serializer = UserProfileSerializer(instance=user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)

    return Response({"errors": ["Modificaicó invàlida"]}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def editProfile(request, id):
    try:
        user = CustomUser.objects.get(id=id)
    except CustomUser.DoesNotExist:
        return Response({"errors": ["L'usuari no existeix."]}, status=status.HTTP_404_NOT_FOUND)

    if request.user != user:
        return Response({"errors": ["No tens permís per actualitzar aquest perfil."]}, status=status.HTTP_403_FORBIDDEN)

    if "picture" not in request.data and "description" not in request.data:
        return Response({"errors": ["No has modificat cap camps"]}, status=status.HTTP_400_BAD_REQUEST)

    update_data = {}
    if "picture" in request.data:
        update_data["picture"] = request.data["picture"]
    if "description" in request.data:
        update_data["description"] = request.data["description"]

    serializer = UserSerializer(instance=user, data=update_data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)

    return Response({"errors": ["Modificaicó invàlida"]}, status=status.HTTP_400_BAD_REQUEST)
