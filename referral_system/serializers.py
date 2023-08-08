from rest_framework import serializers

from .models.models import UserProfile


class ReferralUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ["phone"]


class UserProfileSerializer(serializers.ModelSerializer):

    referred_users = ReferralUsersSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ["phone", "invite_code", "referred_users"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["referred_users"] = ReferralUsersSerializer(
            instance.referred_users.all(), many=True
        ).data
        return representation
