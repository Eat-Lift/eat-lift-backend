from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status

from django.contrib.auth.models import User
from .models import CustomUser, PasswordResetCode, UserProfile, Check

from .serializers import UserSerializer, UserProfileSerializer, CheckSerializer

from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from django.core.mail import EmailMultiAlternatives
from decouple import config
from django.template.loader import render_to_string

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
        return Response({"errors": ["Es requereix el token"]}, status=status.HTTP_400_BAD_REQUEST)

    try:
        idinfo = id_token.verify_oauth2_token(
            google_token,
            google_requests.Request(),
            "73227425624-ffg6valiprbvrkpb46riqu3on8jm25uu.apps.googleusercontent.com"
        )

        google_email = idinfo.get('email')
        google_username = google_email.split('@')[0]
        google_picture = idinfo.get('picture')

        signin = False

        try:
            user = CustomUser.objects.get(email=google_email)
        except CustomUser.DoesNotExist:
            user = CustomUser(username=google_username, email=google_email)
            user.save()
            signin = True

        if google_picture:
            user.picture = google_picture
            user.save()

        token, created = Token.objects.get_or_create(user=user)

        if (signin):
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data,
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data,
            }, status=status.HTTP_200_OK)

    except ValueError:
        return Response({"errors": ["Token invàlid"]}, status=status.HTTP_400_BAD_REQUEST)

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

    if not user.profile_info:
        user.profile_info = UserProfile.objects.create()
        user.save()

    serializer = UserProfileSerializer(instance=user.profile_info, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)

    return Response({"errors": ["Modificació invàlida"]}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getPersonalInformation(request, id):
    try:
        user = CustomUser.objects.get(id=id)
    except CustomUser.DoesNotExist:
        return Response({"errors": ["L'usuari no existeix."]}, status=status.HTTP_404_NOT_FOUND)

    if request.user != user:
        return Response({"errors": ["No tens permís per accedir a aquesta informació personal."]}, status=status.HTTP_403_FORBIDDEN)

    if not user.profile_info:
        return Response({"errors": ["No hi ha informació personal disponible per aquest usuari."]}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserProfileSerializer(user.profile_info)
    return Response({"user": serializer.data}, status=status.HTTP_200_OK)

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

@api_view(['POST'])
def resetPassword(request):
    email = request.data.get('email')
    if not email:
        return Response({"errors": ["Es requereix l'email"]}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response({"errors": ["No existeix cam compte que coincideixi amb l'email introduït"]}, status=status.HTTP_404_NOT_FOUND)

    reset_code = PasswordResetCode.objects.create(user=user)
    
    html_content = render_to_string('password_reset_email.html', {
        'user': user,
        'reset_code': reset_code.code
    })

    email_message = EmailMultiAlternatives(
        subject="Codi de Restabliment de Contrasenya",
        body=f"El teu codi de restabliment de contrasenya és {reset_code.code}. Caduca en 10 minuts.",
        from_email=config('EMAIL_HOST_USER'),
        to=[email]
    )
    email_message.attach_alternative(html_content, "text/html")
    email_message.send()

    return Response({"message": ["Email enviat"]}, status=status.HTTP_200_OK)

@api_view(['POST'])
def newPassword(request):
    email = request.data.get('email')
    reset_code = request.data.get('reset_code')
    new_password = request.data.get('new_password')

    if not email or not reset_code or not new_password:
        return Response({"errors": ["Es requereix l'email, el codi i una nova contrasenya"]}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response({"errors": ["Email invàlid"]}, status=status.HTTP_404_NOT_FOUND)

    try:
        code_entry = PasswordResetCode.objects.get(user=user, code=reset_code)
    except PasswordResetCode.DoesNotExist:
        return Response({"errors": ["El codi és invàlid"]}, status=status.HTTP_400_BAD_REQUEST)

    if not code_entry.is_valid():
        return Response({"errors": ["El codi ha expirat"]}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    code_entry.delete()

    return Response({"message": ["S'ha canviat al contrasenya"]}, status=status.HTTP_200_OK)


# Checks

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createCheck(request, user_id):
    if request.user.id != user_id:
        return Response(
            {"errors": ["Aquest no és el teu usuari"]},
            status=status.HTTP_403_FORBIDDEN
        )

    check_data = request.data
    date = check_data.get('date')

    if not date:
        return Response(
            {"errors": ["Falta la data"]},
            status=status.HTTP_400_BAD_REQUEST
        )

    check, _ = Check.objects.get_or_create(user_id=user_id, date=date)

    all_fields = [field.name for field in Check._meta.get_fields() if field.name not in ('id', 'user')]

    for field in all_fields:
        if field not in check_data:
            setattr(check, field, None)

    serializer = CheckSerializer(instance=check, data=check_data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getCheck(request, user_id):
    if request.user.id != user_id:
        return Response(
            {"errors": ["Aquest no és el teu usuari"]},
            status=status.HTTP_403_FORBIDDEN
        )

    date = request.query_params.get('date', None)

    try:
        if date:
            check = Check.objects.get(user_id=user_id, date=date)
        else:
            check = Check.objects.filter(user_id=user_id).latest('date')

        serializer = CheckSerializer(check)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Check.DoesNotExist:
        return Response(
            {"errors": ["Cap registre trobat per a aquest usuari i data."]},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getCheckDates(request, user_id):
    if request.user.id != user_id:
        return Response(
            {"errors": ["Aquest no és el teu usuari"]},
            status=status.HTTP_403_FORBIDDEN
        )

    dates = Check.objects.filter(user_id=user_id).values_list('date', flat=True).distinct()

    if not dates:
        return Response(
            {"errors": ["No hi ha dates registrades per a aquest usuari."]},
            status=status.HTTP_404_NOT_FOUND
        )

    return Response(list(dates), status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getChecksSummary(request, user_id):
    if request.user.id != user_id:
        return Response(
            {"errors": ["Aquest no és el teu usuari"]},
            status=status.HTTP_403_FORBIDDEN
        )

    checks = Check.objects.filter(user_id=user_id).values('date', 'bodyfat', 'weight')

    if not checks:
        return Response(
            {"errors": ["No s'han trobat registres per a aquest usuari."]},
            status=status.HTTP_404_NOT_FOUND
        )

    return Response(list(checks), status=status.HTTP_200_OK)