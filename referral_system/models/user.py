from .models import UserProfile


def get_user(id=None, phone=None):
    try:
        if id:
            user = UserProfile.objects.get(id=id)
        elif phone:
            user = UserProfile.objects.get(phone=phone)
        return user

    except UserProfile.DoesNotExist:
        return None
