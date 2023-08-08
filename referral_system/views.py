import time

from rest_framework.views import APIView
from rest_framework.response import Response

from .models.models import UserProfile
from .serializers import UserProfileSerializer
from .utils import generate_code, generate_invite_code, authenticate_user
from .jwt_utils import generate_token, jwt_authentication

from django.contrib.auth import login


class PhoneNumberAuthView(APIView):

    @staticmethod
    def post(request):
        phone = request.data["phone"]

        try:
            user = UserProfile.objects.get(phone=phone)
        except UserProfile.DoesNotExist:
            user = UserProfile.objects.create(
                phone=phone, invite_code=generate_invite_code()
            )

        user.confirmation_code = generate_code()
        user.save()

        time.sleep(1)

        return Response(
            {
                "message": "Confirmation code has been sent",
                "confirmation_code": user.confirmation_code,
                "phone": phone,
            }
        )


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


class UserProfileAPIView(APIView):

    @staticmethod
    def get(request):
        user = jwt_authentication(request)

        if not user:
            return Response({"error": "Unauthorized"}, status=401)

        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)


class ReferralAdditionView(APIView):

    @staticmethod
    def post(request):
        user_status = jwt_authentication(request)
        if user_status:
            invite_code = request.data["invite_code"]

            try:
                inviting_user = UserProfile.objects.get(invite_code=invite_code)
            except UserProfile.DoesNotExist:
                return Response({"error": "Invalid invite code"})

            inviting_user.referred_users.add(request.user)
            inviting_user.save()

            return Response({"success": "Referrer added"})
        else:
            return Response({"error": "Unauthorized"}, status=401)
