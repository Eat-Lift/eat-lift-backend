from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status

from django.contrib.auth.models import User
from .models import CustomUser

from .serializer import UserSerializer

from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    serializer = UserSerializer(instance=request.user)

    return Response(serializer.data, status=status.HTTP_200_OK)
