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
    path("api/auth/phone/", PhoneNumberAuthView.as_view()),
    path("api/auth/code/", VerifyCodeView.as_view()),
    path("api/user/profile/", UserProfileAPIView.as_view()),
    path("api/invite/add/", ReferralAdditionView.as_view())
]
