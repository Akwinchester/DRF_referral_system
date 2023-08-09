from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import UserProfileSerializer
from .jwt_utils import generate_token, jwt_authentication
from .services.authentication_user import send_confirmation_code, generate_confirmation_code,\
    create_user, authenticate_user
from .services.referrals_service import add_referal
from django.contrib.auth import login


# Класс для авторизации по номеру телефона
class PhoneNumberAuthView(APIView):

    @staticmethod
    def post(request):
        phone = request.data['phone']

        user = create_user(phone)
        code = generate_confirmation_code(user)
        send_confirmation_code(phone, code)

        return Response({
            'message': 'Code sent',
            'confirmation_code': code,
            'phone': phone,
        })


# Класс для ввода и проверки кода подтверждения
class VerifyCodeView(APIView):

    @staticmethod
    def post(request):
        phone = request.data["phone"]
        confirmation_code = request.data["confirmation_code"]

        user = authenticate_user(phone, confirmation_code)

        if not user:
            return Response({"error": "Invalid code"}, status=400)

        login(request, user)

        token = generate_token(user)

        return Response({"token": token, "phone": phone})


# Класс для получения профиля пользователя
class UserProfileAPIView(APIView):

    @staticmethod
    def get(request):
        user = jwt_authentication(request)

        if not user:
            return Response({"error": "Unauthorized"}, status=401)

        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)


# Класс для добавления реферала
class ReferralAdditionView(APIView):

    @staticmethod
    def post(request):

        user_status = jwt_authentication(request)
        if user_status:
            invite_code = request.data["invite_code"]
            response = add_referal(request=request, invite_code=invite_code)
            return Response(response)

        else:
            return Response({"error": "Unauthorized"}, status=401)
