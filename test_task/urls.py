from django.contrib import admin
from django.urls import path

from referral_system.views import (
    PhoneNumberAuthView, 
    VerifyCodeView,
    UserProfileAPIView,
    ReferralAdditionView
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/phone/", PhoneNumberAuthView.as_view(), name="phone_auth"),
    path("api/auth/code/", VerifyCodeView.as_view(), name="verify_code"),
    path("api/user/profile/", UserProfileAPIView.as_view(), name="user_profile"),
    path("api/invite/add/", ReferralAdditionView.as_view(), name="referral_add"),
]